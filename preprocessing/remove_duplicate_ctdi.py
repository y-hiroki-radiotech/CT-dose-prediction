import pandas as pd
import numpy as np


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
    
    # 複数スキャンの最大値のindexのみ取得する
    max_indices = df_duplicated.groupby('accession')['Mean CTDIvol'].idxmax()
    result_df = df_duplicated.loc[max_indices].reset_index(drop=True)
    df = pd.concat([df_not_duplicated, result_df], axis=0)
    df.reset_index(drop=True, inplace=True)
    
    # 脳CTAでperfusionで撮影したものは名前の変更
    df.loc[df[df['scan protocol'].str.contains('Perfusion')].index, 'scan_area'] = '脳Perfusion'
    
    
    # 副鼻腔はヘッドレストを使ってないものを除く（現在作業中）
    
    df.reset_index(drop=True, inplace=True)
    
    
    # 処理が正常に行われたかどうかprintする
    if unique_data_num == len(df):
        print('正常に処理が行われました。')
        return df
    elif unique_data_num > len(df):
        print('重複処理を削除し過ぎている可能性があります')
    else:
        print('重複処理の削除に失敗しています')
        
    