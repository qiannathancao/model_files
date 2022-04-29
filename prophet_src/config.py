# Path and files
DATA_PATH = 'C:\\Users\\u279014\Documents\\H_Drive\\7.AA Models\\1.CRU_index_fcst\\data'
MODEL_PATH = 'C:\\Users\\u279014\Documents\\H_Drive\\7.AA Models\\1.CRU_index_fcst\\model'
FORECAST_RESULT_PATH = 'C:\\Users\\u279014\Documents\\H_Drive\\7.AA Models\\1.CRU_index_fcst\\result'

# ORIGINAL_FILE = 'FY20 Big Three Dashboard_Nathan_TSModel.xlsx'
ORIGINAL_FILE = 'FY20 Big Three Dashboard.xlsx'
TRAINING_DATA_FILE = 'index.csv'
MODEL_NAME = 'prophet_forecast_model'
CV_FORECAST_OUTPUT = 'CV_forecast.csv'
FORECAST_OUTPUT = '_forecast_result.csv'
METRICS_OUTPUT = '_metrics_result.csv'

# Parameters
PICK_COLS = {'HRC': [1, 3], 'PLATE': [1, 13]}
INDEX_PICK = 'HRC'

FREQ = 'W'
CV_PERIODS = {'W': 48,
              'M': 12,
              'D': 360
              }

YHAT_CLASS = ['yhat', 'yhat_lower', 'yhat_upper']

PREDICTION_PERIOD = {'W': [48, 24, 12, 4],
                     'M': [12, 6, 3, 1],
                     'D': [360, 180, 90, 30]
                     }
