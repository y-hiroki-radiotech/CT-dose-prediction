import pandas as pd


def special_scan_exclude(df):
    
    #　本来140, 120kVを用いない撮影部位で140、120kVで撮影されているものは取り除く
    # 四肢系の特殊撮影Dual energyは件数が少ないので除外する。これは予測しない。
    scan_areas_to_remove = ['側頭骨CT', '顔面骨CT', '副鼻腔CT', '大腿・膝・下腿CT', '胸腰椎CT',
                            '肩・上腕・鎖骨CT', '足・足関節CT', '頸部CT', '肘・前腕・手関節CT',
                            '骨盤骨CT', '脳CTA', '頸椎・頚髄CT', '胸部CT', '胸部〜骨盤CT', '腹部〜骨盤CT',
                            '上腹部CT', '頸部〜骨盤CT']
    kV_values_to_remove = [140, 120, 80]
    
    df = df[~(df['scan_area'].isin(scan_areas_to_remove) & df['kV'].isin(kV_values_to_remove))]
    
    # 歯・顎骨CTは140kVで撮影するので、それ以外は除外する
    kV_values_to_remove = [100, 120]
    df = df[~((df['scan_area'] == '歯・顎骨CT') & (df['kV'].isin(kV_values_to_remove)))]
    
    df.reset_index(drop=True, inplace=True)
    
    return df