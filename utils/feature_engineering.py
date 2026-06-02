import pandas as pd

def create_features(df):

    df["Yield"] = df["Price"]

    df["lag1"] = df["Yield"].shift(1)
    df["lag2"] = df["Yield"].shift(2)
    df["lag3"] = df["Yield"].shift(3)

    df["ma5"] = df["Yield"].rolling(5).mean()
    df["ma20"] = df["Yield"].rolling(20).mean()

    df["volatility"] = (
        df["Yield"]
        .rolling(20)
        .std()
    )

    df["target"] = df["Yield"].shift(-30)

    df.dropna(inplace=True)

    return df