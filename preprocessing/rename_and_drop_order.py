import pandas as pd

def rename_and_drop_order_one_scan_ctdi(df):
    
    # 肺塞栓CTを統一する
    df.loc[df[df['scan_area'].str.contains('肺塞栓')].index, 'scan_area'] = '肺塞栓CT'
    
    # 脳CTAでperfusionで撮影したものは名前の変更
    df.loc[df[df['scan protocol'].str.contains('Perfusion')].index, 'scan_area'] = '脳Perfusion'
    
    # 副鼻腔CT（’ナビゲーション’）は副鼻腔CTへ統一
    df.loc[df[df['scan_area'].str.contains('副鼻腔CT（ﾅﾋﾞｹﾞｰｼｮﾝ）')].index, 'scan_area'] = '副鼻腔CT'
    
    # 脳・顔面骨CTは顔面骨CTへ統一
    df.loc[df[df['scan_area'].str.contains('脳・顔面骨CT')].index, 'scan_area'] = '顔面骨CT'
    
    # 冠動脈の解析、バイパス有、は冠動脈に統一し、1回スキャンの値にCTDIvolを上書きする
    df.loc[df[df['scan_area'].str.contains('冠動脈CT')].index, 'scan_area'] = '冠動脈CT'
    
    # 肺静脈CTのカルト＋解析あり、カルトを肺静脈CTへ統一
    df.loc[df[df['scan_area'].str.contains('肺静脈CT')].index, 'scan_area'] = '肺静脈CT'
    
    # 左右肩、上腕、鎖骨領域をまとめて肩・上腕・鎖骨CTとする。
    df.loc[df[df['scan_area'].str.contains('鎖骨')].index, 'scan_area'] = '肩・上腕・鎖骨CT'
    df.loc[df[df['scan_area'].str.contains('肩')].index, 'scan_area'] = '肩・上腕・鎖骨CT'
    df.loc[df[df['scan_area'].str.contains('上腕')].index, 'scan_area'] = '肩・上腕・鎖骨CT'
    
    # 肘、手、手関節CTは肘・前腕・手関節CTに統一
    df.loc[df[df['scan_area'].str.contains('前腕')].index, 'scan_area'] = '肘・前腕・手関節CT'
    df.loc[df[df['scan_area'].str.contains('手')].index, 'scan_area'] = '肘・前腕・手関節CT'
    df.loc[df[df['scan_area'].str.contains('肘')].index, 'scan_area'] = '肘・前腕・手関節CT'
    
    # 足、趾、足関節は足・足関節CTとする
    df.loc[df[df['scan_area'].str.contains('足')].index, 'scan_area'] = '足・足関節CT'
    
    # 大腿、膝、下腿、その他下肢は大腿・膝・下腿CTとする
    df.loc[df[df['scan_area'].str.contains('腿')].index, 'scan_area'] = '大腿・膝・下腿CT'
    df.loc[df[df['scan_area'].str.contains('膝')].index, 'scan_area'] = '大腿・膝・下腿CT'
    df.loc[df[df['scan_area'].str.contains('下肢')].index, 'scan_area'] = '大腿・膝・下腿CT'
    
    # DICCTを上腹部CTに統一
    df.loc[df[df['scan_area'].str.contains('DICCT（造影）')].index, 'scan_area'] = '上腹部CT'
    
    # 頸部〜胸部CTは頸部〜骨盤CTへ統一する
    df.loc[df[df['scan_area'].str.contains('頸部〜胸部CT')].index, 'scan_area'] = '頸部〜骨盤CT'
    
    # 胸椎・胸髄CTと腰椎・腰髄CTは胸腰椎CTに統一する
    df.loc[df[df['scan_area'].str.contains('胸椎・胸髄CT')].index, 'scan_area'] = '胸腰椎CT'
    df.loc[df[df['scan_area'].str.contains('腰椎・腰髄CT')].index, 'scan_area'] = '胸腰椎CT'
    
    
    # 削除するオーダー名は、左上肢シャントCT,仙椎・尾骨CT,胸骨CT、その他上肢、を削除
    df.drop(index=df[df['scan_area'].str.contains('上肢')].index, inplace=True)
    df.drop(index=df[df['scan_area'].str.contains('仙椎・尾骨CT')].index, inplace=True)
    df.drop(index=df[df['scan_area'].str.contains('胸骨')].index, inplace=True)
    
    # 放射線治療や普段使わない,または稀なプロトコールの排除
    df.drop(index=df[df['scan protocol'].str.contains('9.6 nonHelical 8slice Routine  - 80cm')].index, inplace=True)
    df.drop(index=df[df['scan protocol'].str.contains('6.9 Kunishima')].index, inplace=True)
    df.drop(index=df[df['scan protocol'].str.contains('6.26 Abdomen-Pelvis 4D')].index, inplace=True)
    df.drop(index=df[df['scan protocol'].str.contains('4.12 Hand Tendon 140keV nonHelical')].index, inplace=True)
    
    # 胸部CT、胸部〜骨盤CT、腹部〜骨盤CT,上腹部CT、頸部〜骨盤CTの140kVのDual Energy CTを体幹部Dual Energy CTとしてまとめる。
    # Define the conditions for the change
    scan_areas_to_change = ['胸部CT', '胸部〜骨盤CT', '腹部〜骨盤CT', '上腹部CT', '頸部〜骨盤CT']
    kV_value_to_change = 140
    protocol_to_change = 'GSIX'

    # Make the change in the dataframe
    df.loc[(df['scan_area'].isin(scan_areas_to_change)) & (df['kV'] == kV_value_to_change) & df['scan protocol'].str.contains(protocol_to_change, na=False), 'scan_area'] = '体幹部Dual Energy CT'
    
    # Define the conditions for the change
    scan_method_to_change = 'Dual Energy'
    kV_value_to_change = 100
    new_scan_method = '単純'
    
    # Dual Energyの最終確認
    dual_protocols = df[df['scan protocol'].str.contains('GSIX')]['scan_area'].unique()
    for dual_protocol in dual_protocols:
        if dual_protocol not in ['体幹部Dual Energy CT', '肺塞栓CT']:
            dual_index = df[(df['scan_area'] == dual_protocol) & (df['scan protocol'].str.contains('GSIX'))].index
            df.loc[dual_index, 'scan_area'] = '体幹部Dual Energy CT'
    

    # Make the change in the dataframe
    df.loc[(df['scan_method'] == scan_method_to_change) & (df['kV'] == kV_value_to_change), 'scan_method'] = new_scan_method
    
    df.reset_index(drop=True, inplace=True)
    
    # 冠動脈・肺静脈スキャンを1回あたりのCTDIvolに変更
    df['Mean CTDIvol'] = df.apply(lambda row: row['Mean CTDIvol'] / (row['exposure time'] / row['exposure time per rotation']) if row['scan_area'] == '冠動脈CT' else row['Mean CTDIvol'], axis=1)
    df['Mean CTDIvol'] = df.apply(lambda row: row['Mean CTDIvol'] / (row['exposure time'] / row['exposure time per rotation']) if row['scan_area'] == '肺静脈' else row['Mean CTDIvol'], axis=1)
    
    
    