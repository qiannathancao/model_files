import pandas as pd
import os
import config


def load_data(index_pick):
    data = pd.read_excel(os.path.join(config.DATA_PATH, config.ORIGINAL_FILE), sheet_name='CRU v Platts', skiprows=3,
                         usecols=config.PICK_COLS[index_pick])
    data.columns = ['date', index_pick]
    # print(data[index_pick].isna().sum())
    data[index_pick].fillna(method='ffill', inplace=True)
    # print(data[index_pick].isna().sum())
    data.set_index('date', inplace=True)
    data = data[-data[index_pick].isna()]
    print(f'Nan:{data.isna().sum()}')
    data.to_csv(os.path.join(config.DATA_PATH, config.TRAINING_DATA_FILE))

    ts_month = data.resample('M').mean().astype('int')
    ts_week = data.resample('W').mean().astype('int')
    ts_day = data.resample('D').mean().fillna(method='ffill').astype('int')
    return ts_month, ts_week, ts_day


def traintestsplit(index_pick, freq=config.FREQ):
    ts_month, ts_week, ts_day = load_data(index_pick)
    if freq == 'W':
        ts = ts_week.reset_index()
    elif freq == 'M':
        ts = ts_month.reset_index()
    else:
        ts = ts_day.reset_index()

    ts.columns = ['ds', 'y']
    period = config.CV_PERIODS[freq]
    train = ts.iloc[:-period, :]
    test = ts.iloc[-period:, :]
    return train, test


if __name__ == "__main__":
    train, test = traintestsplit(freq=config.FREQ)
    print(test.tail())
