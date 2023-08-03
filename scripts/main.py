import sys
from io import BytesIO
import tabula 
import pandas as pd

# python __main__.py < 3.pdf

def clean(dataframe):
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe.iloc[1:]
    return dataframe

if __name__ == '__main__':
    df = tabula.read_pdf(BytesIO(sys.stdin.buffer.read()),pages='all',lattice=True)

    final_data_frame = clean(df[0])

    for i in range(1, len(df) - 1):
        final_data_frame = pd.concat([final_data_frame, clean(df[i])])
        final_data_frame.reset_index(drop=True, inplace=True)

    final_data_frame.drop(columns=['S.No.'])

    final_data_frame.rename(columns={
        'S.No.': 's_no',
        'Register No.': 'register_no',
        'Name of the Student': 'name'
    }, inplace=True)

    print(final_data_frame.to_json(orient='records'))