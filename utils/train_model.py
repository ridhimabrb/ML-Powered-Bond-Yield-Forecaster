import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from utils.feature_engineering import create_features

df = pd.read_csv(
    "data/india_10y_yield.csv"
)

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)
df = create_features(df)

features = [
    "lag1",
    "lag2",
    "lag3",
    "ma5",
    "ma20",
    "volatility",
    "Open",
    "High",
    "Low"
]

X = df[features]

y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    shuffle=False,
    test_size=0.2
)

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"MAE: {mae:.4f}")

joblib.dump(
    model,
    "models/random_forest.pkl"
)

print("Model Saved")