import pandas as pd


def drop_emergency_suspicious_height_weight(df):
    """
    この関数は、データフレームから特定の条件に該当する行を削除し、身長と体重の範囲を指定します。

    ファンクションは以下の処理を行います:
    1. 救急科の全データを削除します。
    2. 成人のデータのみを保持します。
    3. scan seriesがNaNとnot NaNのものを分けます。データは装置のバージョンアップにより変更されるため、この分割が必要です。
    4. target regionがHeadのデータは設定変更のため削除します。
    5. 身長が100cm以上200cm未満、体重が20kg以上250kg未満のデータのみを保持します。
    
    Parameters
    ----------
    df : DataFrame
        前処理を行いたいデータフレーム
    
    Returns
    -------
    df_temp : DataFrame
        救急科データが削除され、成人のデータだけが含まれ、特定のscan seriesとtarget regionの行が削除され、
        また、身長と体重が特定の範囲内にあるデータフレーム
    """
    
    # シンプルに救急科を全て削除する
    df_temp = df[~(df['department'] == '救急科')]
    # 成人のみに限定
    df_temp = df_temp[df_temp['adult_child'] == '成人']

    # 次にやるべきことは、scan seriesがNaNとnot NaNになるものを分ける
    # この境界が装置のバージョンアップをしているので、この境界でデータを比較しておく必要がある。
    df_scan_series_nan = df_temp[df_temp['scan series'].isna()]
    df_scan_series_not_nan = df_temp[~df_temp['scan series'].isna()]

    # 頭部の検査は設定を変更しているので、target regionがHeadのものは削除する
    df_scan_series_nan_not_head = df_scan_series_nan[~(df_scan_series_nan['target region'] == 'Head')]

    # データを結合して、reset_index
    df_temp = pd.concat([df_scan_series_nan_not_head, df_scan_series_not_nan], axis=0).reset_index(drop=True)
    
    df_temp = df_temp[(df_temp['height_cm'] > 100) & (df_temp['height_cm'] < 200)]
    df_temp = df_temp[(df_temp['weight_kg'] > 20) & (df_temp['weight_kg'] < 250)]
    
    df_temp.reset_index(drop=True, inplace=True)
    
    return df_temp