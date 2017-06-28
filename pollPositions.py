import pandas as pd
from google.protobuf import json_format
import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime
from matplotlib.pyplot import pause
from .translinkUtilies import tryIntCoerce, convertColumnToType
from .vehicleInformation import *


def pollPositionUpdates(apikey, baseURL):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(baseURL + apikey)
    feed.ParseFromString(response.content)
    position_updates = [json_format.MessageToDict(entity.vehicle)
                        for entity in feed.entity
                        if entity.HasField('vehicle')]
    puCols = ['lat', 'lon', 'ts', 'tid', 'vid']
    position_updates_df = pd.DataFrame([[*getLatLon(pu), getTimestamp(pu),
                                         getTripId(pu), getVehicleId(pu)]
                                        for pu in position_updates],
                                       columns=puCols)
    position_updates_df = convertColumnToType(position_updates_df,
                                              {'tid': 'category',
                                               'vid': 'category'})
    return position_updates_df


def main(apikey, positionUpdateURL, p=150):
    while True:
        print('fetching positions at {}.'.format(datetime.now().isoformat()))
        pu = pollPositionUpdates(apikey, positionUpdateURL)
        print(pu.head())
        print('writing positions to file...')
        with open('./PositionUpdates.csv', 'a', encoding='utf-8') as fp:
            pu.to_csv(fp, index=False, header=False)
        print('waiting for next update...\n')
        pause(p)


if __name__ == '__main__':
    print('Polling TransLink API for bus positions')
    with open('./api.key', 'r+', encoding='utf-8') as fp:
        apikey = fp.read()
    positionUpdateURL = 'http://gtfs.translink.ca/gtfsposition?apikey='
    main(apikey, positionUpdateURL)
