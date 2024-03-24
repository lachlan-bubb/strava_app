import pandas as pd
import plotly.express as px
import sklearn as skl
import xgboost as xgb
import numpy as np
from sklearn.linear_model import LinearRegression


def meters_per_second_to_minutes_per_mile(meters_per_second):
    # 1 mile = 1609.34 meters
    # 1 hour = 3600 seconds
    # 1 mile per hour = 1609.34 meters / 3600 seconds
    meters_per_hour = meters_per_second * 3600
    miles_per_hour = meters_per_hour / 1609.34

    # Convert miles per hour to minutes per mile
    # 1 minute = 1/60 hour
    minutes_per_mile = 1 / miles_per_hour * 60
    return minutes_per_mile


def miles_to_meters(miles):
    meters = miles * 1609.34
    return meters


def meters_to_miles(meters):
    miles = meters / 1609.34
    return miles


def minutes_to_seconds(minutes):
    seconds = minutes * 60
    return seconds


def seconds_to_minutes(seconds):
    minutes = seconds / 60
    return minutes


def model_build_main(df_input):
    df = df_input.copy()
    df = df.sort_values(by="start_date")
    df = df[df["start_date"] >= "2023-08-01"]
    df = df[df["type"] == "Run"]
    df = df.dropna(subset="suffer_score")
    df = df.dropna(subset="average_heartrate")

    df["average_speed"] = meters_per_second_to_minutes_per_mile(df["average_speed"])
    df["max_speed"] = meters_per_second_to_minutes_per_mile(df["max_speed"])
    df["distance"] = meters_to_miles(df["distance"])
    df["moving_time"] = seconds_to_minutes(df["moving_time"])

    # Select train cols
    train_cols = [
        "max_heartrate",
        "average_heartrate",
        "average_speed",
        "moving_time",
    ]  # , 'total_elevation_gain']
    monotone_constraints = {
        "max_heartrate": 0,
        "average_heartrate": 1,
        "average_speed": -1,
        "moving_time": 1,
    }  # [0, -1, 0, -1, 1]  # Example constraints for 5 features

    # Split the data into training and testing sets
    X = df[train_cols]
    y = df["suffer_score"]

    # Split at random
    # X_train, X_test, y_train, y_test = skl.model_selection.train_test_split(X, y, test_size=0.2, random_state=5)

    # Select the most recent rows (e.g., 80% for training and 20% for testing)
    split_point = int(0.7 * len(df))
    X_train = X.iloc[:split_point]
    X_test = X.iloc[split_point:]
    y_train = y.iloc[:split_point]
    y_test = y.iloc[split_point:]

    # Instantiate an XGBoost classifier
    model = xgb.XGBRegressor(
        learning_rate=0.3,
        n_estimators=50,
        max_depth=3,
        monotone_constraints=monotone_constraints,
    )

    eval_set = [(X_train, y_train), (X_test, y_test)]

    # apply monotonic contstraints

    # Train the model on the training data
    model.fit(
        X_train,
        y_train,
        eval_set=eval_set,
        eval_metric="rmse",
        early_stopping_rounds=10,
        verbose=True,
    )

    # Make predictions on the test data
    # y_pred = model.predict(X_test)

    # Make predictions on the training and test data
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Calculate Mean Squared Error (MSE) for training and test data
    train_mse = skl.metrics.mean_squared_error(y_train, y_train_pred)
    test_mse = skl.metrics.mean_squared_error(y_test, y_test_pred)
    print("Train R Mean Squared Error:", np.sqrt(train_mse))
    print("Test R Mean Squared Error:", np.sqrt(test_mse))

    print("Best iteration: ", model.best_iteration)

    # Heart rate model
    model_heartrate = LinearRegression()
    model_heartrate.fit(
        np.square(df["average_speed"].values).reshape(-1, 1),
        df["average_heartrate"].values,
    )

    # Prep for scoring
    # Calculate the average of each column
    averages = X.mean()
    print(averages)
    x_pred = pd.DataFrame(averages).transpose()

    model_object = {
        "model": model,
        "model_heartrate": model_heartrate,
        "x_pred": x_pred,
    }

    return model_object


def model_score(model_object, distance, speed):
    distance = pd.to_numeric(distance)
    speed = pd.to_numeric(speed)

    model = model_object["model"]
    model_heartrate = model_object["model_heartrate"]
    x_pred = model_object["x_pred"]

    heartrate_pred = model_heartrate.predict(
        pd.DataFrame({"average_speed": [np.square(speed)]})
    )

    if "average_heartrate" in x_pred.columns:
        x_pred["average_heartrate"] = heartrate_pred

    if "average_speed" in x_pred.columns:
        x_pred["average_speed"] = speed  # minutes per mile

    if "moving_time" in x_pred.columns:
        x_pred["moving_time"] = distance * speed  # miles * minutes per mile

    if "distance" in x_pred.columns:
        x_pred["distance"] = distance

    pred_value = model.predict(x_pred)

    return pred_value
