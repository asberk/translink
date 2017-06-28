def tryIntCoerce(x):
    try:
        x = int(x)
    except ValueError as ve:
        pass
    return x


def convertColumnToType(df, colTypeDict):
    for col, newType in colTypeDict.items():
        df[col] = df[col].astype(newType)
    return
