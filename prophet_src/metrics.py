import preprocessing as pp
import pandas as pd
import numpy as np
import os
import config
import train_prophet as tp
from sklearn.metrics import mean_absolute_error


def run_metrics(index_pick):
    train_set, test_set = pp.traintestsplit(index_pick, freq=config.FREQ)
    tp.run_training(train_set)
    forecast = tp.run_test_predict()
    col_loc = [forecast.columns.get_loc(x) for x in config.YHAT_CLASS]
    forecast = forecast[-config.CV_PERIODS[config.FREQ]:]

    metrics = []
    for i in col_loc:
        metrics_boundary = []
        for p in config.PREDICTION_PERIOD[config.FREQ]:
            mae = mean_absolute_error(test_set.y[:p], forecast.iloc[:p, i])
            metrics_boundary.append(mae)
        metrics.append(metrics_boundary)
    res = pd.DataFrame(metrics, index=forecast.columns[col_loc], columns=config.PREDICTION_PERIOD[config.FREQ])
    res['average_mae'] = res.mean(axis=1)
    res.to_csv(os.path.join(config.FORECAST_RESULT_PATH, index_pick+config.METRICS_OUTPUT), index=False)
    forecast_col = res.index[np.argmin(res.average_mae)]
    return forecast_col
