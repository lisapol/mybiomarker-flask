import os
import pandas as pd


def transform_blood_profile():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    df = pd.read_csv (f'{dir_path}/my_data.csv')

    df = df[
        ["id","test_dt","test_name_eng","test_results","test_norm_min","test_norm_max","test_unit_eng"]
    ]
    ##Convert number strings to floats
    df = df.apply(pd.to_numeric, errors='ignore')
    df['test_dt'] = pd.to_datetime(df['test_dt']).dt.strftime('%Y-%m-%d')
    # drop duplicates and keep row with max values
    df = df.sort_values('test_results', ascending=False)
    return df


def transform_menstrual_data():
    df_menstrual_data = [
    {'id': 4, 'period_start': '2022-08-09', 'period_end': '2022-08-14',},
    {'id': 5, 'period_start': '2022-10-20', 'period_end': '2022-10-25',},
    {'id': 6, 'period_start': '2023-01-05', 'period_end': '',},
    {'id': 7, 'period_start': '2021-01-16', 'period_end': '2021-01-20',},
    {'id': 8, 'period_start': '2021-02-19', 'period_end': '2021-02-24',},
    {'id': 9, 'period_start': '2021-03-27', 'period_end': '2021-04-01',},
    {'id': 10, 'period_start': '2021-05-04', 'period_end': '2021-05-09',},
    {'id': 11, 'period_start': '2021-06-07', 'period_end': '2021-06-12',}]

    df_menstrual = pd.DataFrame(df_menstrual_data, columns=[
        'id',
        'period_start',
        'period_end',
    ]
    )

    df_menstrual['period_end'] = pd.to_datetime(df_menstrual['period_end'])
    df_menstrual['period_start'] = pd.to_datetime(df_menstrual['period_start'])

    df_menstrual['period_length'] = (df_menstrual['period_end'] - df_menstrual['period_start']) + pd.Timedelta(days=1)

    df_menstrual_sorted = df_menstrual.sort_values(by=['period_start', 'period_end'], ascending=True)

    df_menstrual_sorted['cycle_end'] = df_menstrual_sorted.period_start.shift(-1) - pd.Timedelta(days=1)

    df_menstrual_sorted['cycle_end'] = pd.to_datetime(df_menstrual_sorted['cycle_end'])

    df_menstrual_sorted['cycle_length'] = (df_menstrual_sorted['cycle_end'] - df_menstrual_sorted[
        'period_start']) + pd.Timedelta(days=1)

    df_menstrual_sorted['period_length'] = df_menstrual_sorted['period_length'].dt.days

    df_menstrual_sorted['cycle_length'] = df_menstrual_sorted['cycle_length'].dt.days

    df_menstrual_sorted = df_menstrual_sorted.dropna()
    return df_menstrual_sorted
