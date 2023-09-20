import pandas as pd
import numpy as np


def split_aggregated_scans(df, accession_list):
    """この関数は単純＋造影2相のようなスキャンの場合に、造影2相が加算されてしまうRDSRの現象に対応するもの
    　　　　　　加算されてしまったデータに対して、1スキャンに分離するためのものです。
    """
    
    protocol_list = ['5.10 Chest - Pelvis (40sec,80sec)Routine','5.11 Chest - Pelvis (40sec,80sec)Routine','5.12 Chest - Pelvis (40sec,80sec)Routine']
    for accession in accession_list:
        df_subset = df[df['accession'] == accession]
        if df_subset['scan protocol'].unique()[0] in protocol_list:
            min_ctdi = df_subset['Mean CTDIvol'].min()
            max_ctdi = df_subset['Mean CTDIvol'].max()
            if 1.5 < max_ctdi:
                df_subset_index = df_subset.index
                min_ctdi_index = df_subset[df_subset['Mean CTDIvol'] == min_ctdi].index
                rest_index = list(set(df_subset_index) - set(min_ctdi_index))
                df.loc[rest_index, 'Mean CTDIvol'] = df_subset.loc[rest_index]['Mean CTDIvol'] / len(df_subset.loc[rest_index])


def remove_duplicate_ctdi(df):
    """この関数は、読み込んだデータフレームの複数回スキャンした検査のCTDIのうち最大値のスキャンデータを残します。
    　　　　　　単独スキャンデータにデータを結合したデータフレームを返す
    """
    # prepと脂肪測定はnomial total collimation widthが5であることに注目して除外する
    df = df[~(df['nomial total collimation width'] == 5)]
    
    # 側頭骨の管電流調整したものは除く
    df_inner = df[df['scan_area'].str.contains('側頭骨')]
    df_not_inner = df[~df['scan_area'].str.contains('側頭骨')]

    df_inner = df_inner[df_inner['max mA'] < 400]
    df = pd.concat([df_not_inner, df_inner])
    
    
    unique_data_num = len(df['accession'].unique())
    
    # 重複データの抽出
    df_duplicated = df[df['accession'].duplicated(keep=False)]
    
    # 重複なしデータの抽出
    df_not_duplicated = df[~df['accession'].duplicated(keep=False)]
    
    # 重複データのaccessionの集合を作成
    duplicated_accession_set = set(df_duplicated['accession'])
    
    # 造影相の加算に対応するための処理を追加
    split_aggregated_scans(df_duplicated, duplicated_accession_set)
    
    # 複数スキャンの最大値のindexのみ取得する
    max_indices = df_duplicated.groupby('accession')['Mean CTDIvol'].idxmax()
    result_df = df_duplicated.loc[max_indices].reset_index(drop=True)
    df = pd.concat([df_not_duplicated, result_df], axis=0)
    df.reset_index(drop=True, inplace=True)
    
    
    # 副鼻腔はヘッドレストを使ってないものを除く（現在作業中）
    
    
    # 処理が正常に行われたかどうかprintする
    if unique_data_num == len(df):
        print('正常に処理が行われました。')
        return df
    elif unique_data_num > len(df):
        print('重複処理を削除し過ぎている可能性があります')
    else:
        print('重複処理の削除に失敗しています')
        
    