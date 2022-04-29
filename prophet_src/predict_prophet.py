import preprocessing as pp
import os
import config
import train_prophet as tp
import metrics as mt


def predict(index_pick, freq=config.FREQ):
    ts_month, ts_week, ts_day = pp.load_data(index_pick)
    if freq == 'W':
        ts = ts_week.reset_index()
    elif freq == 'M':
        ts = ts_month.reset_index()
    else:
        ts = ts_day.reset_index()
    ts.columns = ['ds', 'y']
    tp.run_training(ts)
    res = tp.run_test_predict()
    return res


if __name__ == "__main__":
    for index_name in config.PICK_COLS.keys():
        forecast = predict(index_pick=index_name)
        forecast_col = mt.run_metrics(index_pick=index_name)
        forecast = forecast.loc[:, ['ds', forecast_col]]
        forecast_month = forecast.set_index(keys='ds').resample('M').mean().reset_index()
        forecast_month['ds'] = forecast_month['ds'].apply(lambda x: str(x.year) + '_' + str(x.month_name()))
        forecast_month.to_csv(os.path.join(config.FORECAST_RESULT_PATH, index_name + config.FORECAST_OUTPUT),
                              index=False)

