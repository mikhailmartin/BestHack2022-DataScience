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

data = pd.read_csv(os.path.join('data', 'transactions.csv'), dtype=dtypes, parse_dates=['datetime'])

for id_a, data_by_id_a in data.groupby('id_a'):
    data_by_id_a.to_csv(os.path.join('data', 'transactions_by_id', f'id_a={id_a}.csv'), index=False)
