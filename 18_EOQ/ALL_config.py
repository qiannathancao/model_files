import numpy as np
UPLOAD_FILE_PATH = r'S:\OSK-Share\DEPT\LOGISTICS\LC3\Projects\Logistics Optimization Tool\Files for Nate to Upload - VOP\1. SAVINGS ANALYSES\Austin - VOP Projects\OPEN Projects\JLG_EOQ'
RESULT_SAVE_PATH = r'S:\OSK-Share\DEPT\LOGISTICS\LC3\Projects\Logistics Optimization Tool\Files for Nate to Upload - VOP\1. SAVINGS ANALYSES\Austin - VOP Projects\OPEN Projects\JLG_EOQ'

UPLOAD_FILE_NAME = r'JLG_EOQ_Rev_3_TEST_single_item.xlsx'

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
carrying_financial_rate = 0.0705
EAU_CALENDER_DAYS = 320