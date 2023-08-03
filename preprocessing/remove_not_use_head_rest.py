import pandas as pd

def remove_not_use_head_rest(df_orig, df_brain, df_inner):
    
    
    # ヘッドレストを使って撮影していないデータを削除する
    df_brain = df_brain[['accession', 'head rest']]
    df_inner = df_inner[['accession', 'head rest']]
    df_concat = pd.concat([df_brain, df_inner], axis=0)
    df = pd.merge(left=df_orig, right=df_concat, how='left', on='accession')
    df_1 = df[df['head rest'].isna()]
    df_2 = df[df['head rest'] == 'T']
    df_3 = df[df['head rest'] == 1.0]
    df = pd.concat([df_1, df_2, df_3])
    df.drop('head rest', axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df