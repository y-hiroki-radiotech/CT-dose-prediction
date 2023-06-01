import pandas as pd
import numpy as np

def preprocess_import_data(df):
    """この関数は、読み込んだデータを整形して、列名を変更する関数です.
    
    params:
        df: 読み込んだDataFrame
        
    Return:
        df: データ整形後のDataFrame
    """
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # 予測に不要な特徴量を削除する
    # 実施検査日、study_date, accessionno, 患者ID, プリセット名称は削除
    drop_list = ['実施検査日(YYYYMMDD)', 'study_date', 'ACCESSIONNO', '患者ID', 'プリセット名称', 'DLP']
    df.drop(drop_list, axis=True, inplace=True)
    
    # column名を変更する
    df.rename(columns={'検査時年齢': 'age', '性別': 'gender', '身長（ｃｍ）': 'height_cm', '体重（ｋｇ）': 'weight_kg',
                       '依頼科名称': 'department', '入院病棟名称': 'hospital_ward', '実施検査室名称': 'room', '撮影機種': 'modality', 
                       '部位名称': 'scan_area', '検査方法': 'scan_method'}, inplace=True)
    # 予測に使う装置
    df.query('modality == "Revolution"', inplace=True)
    
    # 現状ではroom, modalityは１つだけを想定しているので、dropする。
    df.drop(['room', 'modality'], axis=1, inplace=True)

    # hospital_wardのNaNは'外来'を意味する
    df.loc[df['hospital_ward'].isna(), 'hospital_ward'] = '外来'
    
    df.reset_index(inplace=True)
    df.drop(['index', 'kV', 'rotation_time', 'scan_protocol', 'scan_series'], axis=1, inplace=True)
    