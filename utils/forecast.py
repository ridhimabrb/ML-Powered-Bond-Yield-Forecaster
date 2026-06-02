import pandas as pd
import joblib

from utils.feature_engineering import create_features

def forecast_yield():

    model = joblib.load(
        "models/random_forest.pkl"
    )

    df = pd.read_csv(
        "data/india_10y_yield.csv"
    )

    engineered = create_features(df)

    latest = engineered.iloc[-1]

    features = [[
        latest["lag1"],
        latest["lag2"],
        latest["lag3"],
        latest["ma5"],
        latest["ma20"],
        latest["volatility"],
        latest["Open"],
        latest["High"],
        latest["Low"]
    ]]

    prediction = model.predict(features)

    return float(prediction[0])

def latest_yield():

    df = pd.read_csv(
        "data/india_10y_yield.csv"
    )

    return float(
        df["Price"].iloc[-1]
    )