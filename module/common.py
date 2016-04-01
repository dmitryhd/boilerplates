#!/usr/bin/env python3

import pandas as pd


def df_to_csv(dataframe: pd.DataFrame, csv_file_name: str):
    """
    Save dataframe to given location as csv.
    Can deal with utf8 issues.
    """
    header = '|'.join(dataframe.columns.values) + '\n'
    header = header.encode('utf8', 'ignore')  # bytes
    csv_string = header
    # We can deal with very large dataframes, so decode in parts
    chunk = dataframe.to_csv(sep='|', header=False, index=False,
                             encoding='utf-8')
    chunk = chunk.encode('utf8', 'ignore')
    csv_string += chunk
    with open(csv_file_name, 'wb') as wb:
        wb.write(csv_string)

def csv_to_df(csv_file_name: str, sep='|'):
    return pd.read_csv(csv_file_name, sep=sep, header=0)
