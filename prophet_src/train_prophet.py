from fbprophet import Prophet
import config
import joblib
import os
import pandas as pd


def run_training(train_set):
    prophet_basic = Prophet(changepoint_prior_scale=0.08)
    prophet_basic.fit(train_set)
    joblib.dump(prophet_basic, os.path.join(config.MODEL_PATH, config.MODEL_NAME))


def run_test_predict():
    _prophet_model = joblib.load(os.path.join(config.MODEL_PATH, config.MODEL_NAME))
    future = _prophet_model.make_future_dataframe(periods=config.CV_PERIODS[config.FREQ], freq=config.FREQ)
    forecast = _prophet_model.predict(future)
    pd.DataFrame(forecast).to_csv(os.path.join(config.FORECAST_RESULT_PATH, config.CV_FORECAST_OUTPUT), index=False)
    return forecast


