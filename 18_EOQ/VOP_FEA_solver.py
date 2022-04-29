import numpy as np
import pandas as pd
import os
import FEA_config
import re

class solver():
    def __init__(self):
        pass

    def col_name(self, df):
        """
        this is to trim the data_frame column names to a unique format:
        all case, replace space to underscore, remove parentheses
        param df:
            raw from share drive for
        return:
            polished data set with new column names
        """
        df.columns = df.columns.str.strip().str.lower().str.replace('-', '').str.replace(' ', '_').str.replace('(', ''). \
            str.replace(')', '').str.replace('"', '')
        return df

    def pricing_break_generator(self, df):
        pricing_break_keys = [k for k in df.columns if 'piece_bucket' in k]
        pricing_range_start = [int(re.search(r'\d+', c).group()) for c in pricing_break_keys]
        pricing_range_end = pricing_range_start[1:] + [np.inf]
        pricing_break_values = list(zip(pricing_range_start, pricing_range_end))
        pricing_break = dict(list(zip(pricing_break_keys, pricing_break_values)))
        return pricing_break

    def preprocess_fill_na(self, df, pricing_break):
        df_all = df.copy()
        first_pricing_bucket = list(pricing_break.keys())[0]
        last_pricing_bucket = list(pricing_break.keys())[-1]

        df_price = df_all.loc[:, first_pricing_bucket: 'standard_cost'].replace({0: np.nan})
        for index, row in df_price.iterrows():
            if row.isnull().all():
                df_all.loc[index, first_pricing_bucket: last_pricing_bucket] = df_all.loc[index, 'standard_cost']
            elif not np.isnan(row[0]):
                df_all.loc[index, first_pricing_bucket: last_pricing_bucket] = row.ffill()
            else:
                valid_col_index = row.first_valid_index()
                df_all.loc[index, first_pricing_bucket: valid_col_index] = row[valid_col_index]
                df_all.loc[index, valid_col_index:] = row[valid_col_index:].ffill()
        return df_all

    def get_vop_qty(self, pricing_row, vop_day=1):
        """
        pricing_row: data series, single entire row from df_result
        vop_days: iterating from days selection
        """
        vop_qty = (pricing_row['eau'] / FEA_config.EAU_CALENDER_DAYS) * vop_day
        return int(vop_qty) + 1

    def get_order_qty(self, pricing_row, vop_qty):
        """
        pricing_row: data series, single entire row from df_result
        vop_qty: iterated qty from VOP days calculation
        """
        mlpq = pricing_row['multiple_order_qty']
        minq = pricing_row['minimum_reorder_qty']

        if (mlpq == 0) & (minq == 0):
            vopq = vop_qty

        elif (mlpq == 0) & (minq != 0):
            vopq = max(vop_qty, minq)

        elif (minq == 0) & (mlpq != 0):
            if vop_qty <= mlpq:
                vopq = mlpq
            else:
                vopq = ((vop_qty // mlpq) + 1) * mlpq

        else:
            if mlpq <= minq:
                if vop_qty <= minq:
                    vopq = ((minq // mlpq) + 1) * mlpq
                else:
                    vopq = ((vop_qty // mlpq) + 1) * mlpq

            else:
                if vop_qty < mlpq:
                    vopq = mlpq
                else:
                    vopq = ((vop_qty // mlpq) + 1) * mlpq
        return vopq

    def get_unit_cost(self, pricing_row, pricing_break, order_qty):
        """
        pricing_row: data series, single entire row from df_result
        pricing_break: dictionary: pricing category with breaking range
        order_qrt: is vopq after comapring with MOQ & MINQ iterated qty from VOP days calculation

        return: unit_cost: pricing from break bucket
        """
        for key, value in pricing_break.items():
            if (value[0] <= order_qty) and (order_qty < value[1]):
                unit_cost = pricing_row[key]
                return key, unit_cost
        return None

    def get_purchasing_cost(self, unit_cost, pricing_row):
        """
        unit_cost: int, result from pricing break
        pricing_row: data series, single entire row from df_result
        return: total purchasing cost per item
        """
        purchasing_cost = unit_cost * pricing_row['eau']
        return round(purchasing_cost, 2)

    def get_order_frequency(self, order_qty, pricing_row):
        """
        order_qty: ordering qty result from function get_order_qty
        pricing_row: data series, single entire row from df_result
        return:
        """
        order_frequency = min(pricing_row['eau'] / order_qty, 52)
        return round(order_frequency, 2)

    def get_holding_cost(self, purchasing_cost, order_frequency, financial_rate=0.125):
        financial_carrying_frequency = max(order_frequency, 365/83)
        holding_cost = purchasing_cost * financial_rate / financial_carrying_frequency 
        return round(holding_cost, 2)

    def get_logistic_cost(self, order_frequency):
        logistic_cost = order_frequency * 38 / 5
        return round(logistic_cost, 2)

    def get_optimal_vops(self, pricing_row, vop_bound=[], financial_rate=0.073, pricing_break=None):

        cost_dict = {'purchasing_cost': [],
                     'holding_cost': [],
                     'logistic_cost': [],
                     'total_cost': []}

        unit_cost_list = []
        min_combined_cost = np.inf
        optimal_vop_day = 0
        optimal_vop_qty = 0
        optimal_vop_freq = 0

        # while vop_day < 84:
        for vop_day in range(vop_bound[0], vop_bound[1]):  # due to maximum order frequency is 52, hence vop_day starts on 7 days

            vop_qty = self.get_vop_qty(pricing_row=pricing_row, vop_day=vop_day)
            order_qty = self.get_order_qty(pricing_row=pricing_row, vop_qty=vop_qty)
            pricing_bucket, unit_cost = self.get_unit_cost(pricing_row, pricing_break, order_qty=order_qty)
            purchasing_cost = self.get_purchasing_cost(unit_cost=unit_cost, pricing_row=pricing_row)
            order_frequency = self.get_order_frequency(order_qty, pricing_row)
            holding_cost = self.get_holding_cost(purchasing_cost, order_frequency=order_frequency,
                                                 financial_rate=financial_rate)
            logistic_cost = self.get_logistic_cost(order_frequency)
            combined_cost = round((purchasing_cost + holding_cost + logistic_cost), 2)
            if combined_cost <= min_combined_cost:
                min_combined_cost = combined_cost
                optimal_vop_day = vop_day
                optimal_vop_qty = order_qty
                optimal_vop_freq = order_frequency
                optimal_unit_cost = unit_cost

            unit_cost_list.append(unit_cost)

            cost_dict['purchasing_cost'].append(purchasing_cost)
            cost_dict['holding_cost'].append(holding_cost)
            cost_dict['logistic_cost'].append(logistic_cost)
            cost_dict['total_cost'].append(combined_cost)

        return optimal_vop_day, optimal_vop_qty, optimal_vop_freq, optimal_unit_cost


if __name__ == '__main__':
    '''download data from share drive for uploading to model'''
    input_file_path = FEA_config.UPLOAD_FILE_PATH
    input_file_name = FEA_config.UPLOAD_FILE_NAME
    upload_file = os.path.join(input_file_path, input_file_name)
    print(f'Step 1. check upload file name: >>> {upload_file}')

    ''''call class solver for computing'''
    solver = solver()
    df_pricing = solver.col_name(pd.read_excel(upload_file))
    print(f'Step 2. check upload file size: >>> {df_pricing.shape[0]} rows, {df_pricing.shape[1]} columns')


    pricing_break = solver.pricing_break_generator(df_pricing)
    print(f'pricing_break generated as: {pricing_break}')

    df_result = solver.preprocess_fill_na(df_pricing,pricing_break=pricing_break)
    # assert sum(df_result.loc[:, '1_piece_bucket': 'standard_cost'].isna().sum()) == 1
    sum_zero_check = 'process successful' \
        if sum(df_result.loc[:, '1_piece_bucket': 'standard_cost'].isna().sum()) == 0 \
        else 'something wrong'
    print(f'Step 3. check missing price filled in: >>> {sum_zero_check}')

    '''Process in batch material file'''
    print(f'start solving...')
    vop_master_run = df_result.copy()
    vop_master_run[['optimal_vop_day', 'optimal_vop_qty', 'optimal_vop_freq', 'optimal_pricing_bucket']] = \
        vop_master_run.apply(lambda row: solver.get_optimal_vops(row,
                                                                 vop_bound=FEA_config.vop_bound,
                                                                 financial_rate=FEA_config.FEA_carrying_financial_rate,
                                                                 pricing_break=pricing_break)
        if row['eau'] != 0 else 0, axis=1, result_type='expand')

    vop_master_run.to_excel(os.path.join(FEA_config.RESULT_SAVE_PATH, '(result)_'+FEA_config.RESULT_FILE_NAME),
                            index=False)
    print(f'Step 4. problem solved, result saved as {FEA_config.RESULT_FILE_NAME}')
    print(f'>>> Successful. process completed')















