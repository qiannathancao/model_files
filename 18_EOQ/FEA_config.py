import numpy as np
UPLOAD_FILE_PATH = 'S:\\OSK-Share\\DEPT\\LOGISTICS\\LC3\\Projects\\Logistics Optimization Tool\\Files for Nate to Upload - VOP\\VOP_Uploading\\FAE_uploading'
RESULT_SAVE_PATH = 'S:\\OSK-Share\\DEPT\\LOGISTICS\\LC3\\Projects\\Logistics Optimization Tool\\Files for Nate to Upload - VOP\\VOP_Result\\FEA_result'

UPLOAD_FILE_NAME = 'NEW-pricing_loading_ECI and HP Prod_PMI - Copy.xlsx'
RESULT_FILE_NAME = 'NEW-pricing_loading_ECI and HP Prod_PMI - Copy.xlsx'

# PRICING_BREAK = {'1_piece_bucket': [1, 2],
#                  '2_piece_bucket': [2, 5],
#                  '5_piece_bucket': [5, 6],
#                  '6_piece_bucket': [6, 16],
#                  '16_piece_bucket': [16, 25],
#                  '25_piece_bucket': [25, 31],
#                  '31_piece_bucket': [31, 51],
#                  '51_piece_bucket': [51, 101],
#                  '101_piece_bucket': [101, np.inf]}

vop_bound = [7, 84]
FEA_carrying_financial_rate = 0.1
EAU_CALENDER_DAYS = 320