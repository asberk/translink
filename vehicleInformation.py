def getLatLon(pu):
    return tuple(pu['position'][x] for x in ['latitude', 'longitude'])


def getTimestamp(pu):
    return tryIntCoerce(pu['timestamp'])


def getTripId(pu):
    return pu['trip']['tripId']


def getVehicleId(pu):
    return pu['vehicle']['id']
