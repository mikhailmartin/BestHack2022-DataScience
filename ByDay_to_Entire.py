import os
import pandas as pd


dtypes = {
    'time_zone': 'int8',
    'forward': 'int8',
    'zero_call_flg': 'int8',
    'source_b': 'int8',
    'source_f': 'int8',
    'num_b_length': 'int8',
    'duration': 'int16',
}

data = []
for file_name in os.listdir(os.path.join('data', 'transactions_by_day')):
    data.append(pd.read_csv(os.path.join('data', 'transactions_by_day', file_name), dtype=dtypes))
data = pd.concat(data)

data['datetime'] = pd.to_datetime(data['time_key'] + ' ' + data['start_time_local'])
del data['time_key']
del data['start_time_local']

data.to_csv(os.path.join('data', 'transactions.csv'), index=False)
