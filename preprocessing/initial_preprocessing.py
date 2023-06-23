import pandas as pd


def initial_preprocessing(df):
    
    """
    この関数は、医療関連のデータフレームに対して初期の前処理を実施します。

    具体的には以下の処理を行います：
    1. カラム名の変更：特定のカラム名をよりわかりやすい英語の名前に変更します。
    2. 不要なカラムの削除：特定のカラム（例：'患者ID', '検査方法名称', '生年月日（YYYYMMDD）'等）を削除します。
    3. 特定の撮影機種に対するデータの選択：'modality'が'Revolution'の行だけを選択します。
    4. 特定のカラムの削除：'room'カラムを削除します。
    5. NaNの補完：'hospital_ward'カラムのNaNは'外来'に変更します。
    6. `scan protocol` 列が "GSIX" を含むデータは `scan_method` 列の値を "Dual Energy" に変更します。
    7. `pitch factor` 列が NaN のデータは 1.0 に置換します。


    Parameters
    ----------
    df : DataFrame
        前処理対象のデータフレーム。検査時年齢、性別、身長、体重、依頼科名称、入院病棟名称、実施検査室名称、
        撮影機種、プリセット名称、部位名称、検査方法、ACCESSIONNO、患者ID、検査方法名称、生年月日、
        検査責任者名称、撮影進捗、検査種別名称、検査/撮影情報01、検査/撮影情報02などのカラムが含まれていることを想定しています。

    Returns
    -------
    df : DataFrame
        前処理後のデータフレーム。カラム名の変更、不要なカラムの削除、特定の撮影機種のデータ選択、
        'room'カラムの削除、'hospital_ward'のNaN補完が行われます。

    """
    
    # rename用の関数の作成
    columns = columns={'検査時年齢': 'age', '性別': 'gender', '身長（ｃｍ）': 'height_cm', '体重（ｋｇ）': 'weight_kg',
                        '依頼科名称': 'department', '入院病棟名称': 'hospital_ward', '実施検査室名称': 'room', 
                       '撮影機種': 'modality', 'プリセット名称': 'preset_name', '実施検査日(YYYYMMDD)': 'study_date',
                        '部位名称': 'scan_area', '検査方法': 'scan_method', 'ACCESSIONNO': 'accession', '患者ID': 'id', }
    drop_list = ['検査方法名称', '生年月日（YYYYMMDD）', '検査責任者名称',
                 '撮影進捗', '検査種別名称', '検査/撮影情報01', '検査/撮影情報02', 'study_date']
    df.drop(drop_list, axis=1, inplace=True)
    df.rename(columns=columns, inplace=True)
    
    # 予測に使う装置
    df.query('modality == "Revolution"', inplace=True)
    # scan対象を選択したら、roomは落としてしまう
    df.drop('room', axis=1, inplace=True)
    
    # hospital_wardのNaNは外来に変更する
    df.loc[df['hospital_ward'].isna(), 'hospital_ward'] = '外来'
    
    # GSIXのスキャンはDual Energyとして判定
    dual_index = df[df['scan protocol'].str.contains('GSIX')].index.to_list()
    df.loc[dual_index, 'scan_method'] = 'Dual Energy'
    
    # pitch factorがNaNはコンベンショナルスキャンであるので、pitch factorに１を代入する
    df['pitch factor'].fillna(1.0, inplace=True)

    
    df.reset_index(drop=True, inplace=True)