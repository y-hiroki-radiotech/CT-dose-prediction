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
    
    
    # 削除するオーダー名は、左上肢シャントCT,仙椎・尾骨CT,胸骨CT、その他上肢、を削除
    df.drop(index=df[df['scan_area'].str.contains('上肢')].index, inplace=True)
    df.drop(index=df[df['scan_area'].str.contains('仙椎・尾骨CT')].index, inplace=True)
    df.drop(index=df[df['scan_area'].str.contains('胸骨')].index, inplace=True)
    
    df.reset_index(drop=True, inplace=True)
    
    # 冠動脈・肺静脈スキャンを1回あたりのCTDIvolに変更
    df['Mean CTDIvol'] = df.apply(lambda row: row['Mean CTDIvol'] / (row['exposure time'] / row['exposure time per rotation']) if row['scan_area'] == '冠動脈CT' or row['scan_area'] == '肺静脈' else row['Mean CTDIvol'], axis=1)
    
    
    