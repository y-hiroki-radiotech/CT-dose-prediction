import pandas as pd


# BMIを使った分類を作成する
def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'under weight'
    elif bmi < 24.9:
        return 'normal weight'
    elif bmi < 29.9:
        return 'obesity class1'
    elif bmi < 34.9:
        return 'obesity class2'
    elif bmi < 39.9:
        return 'obesity class3'
    return 'obesity class4'


def calculate_bsa(height_cm, weight_kg):
    bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)
    return bsa


def calculate_bmi_bmr_bsa_category(df):
    
    """
    入力となるデータフレームの各レコードに対してBMI、BMR、およびBMIのカテゴリを計算します。

    この関数は、'bmi'、'bmr'、'category_bmi'という3つの新しい列をデータフレームに追加します。
    'bmi'はBody Mass Index（体格指数）、'bmr'はBasal Metabolic Rate（基礎代謝率）、'category_bmi'はBMIのWHO基準による分類を意味します。

    Parameters
    ----------
    df : DataFrame
        入力となるデータフレームです。'weight_kg'（体重）、'height_cm'（身長）、'gender'（性別）、'age'（年齢）という列が必要です。
        体重の単位はkg、身長はcm、年齢は年であるべきです。性別は男性を'M'、女性を'F'で表すことを想定しています。

    Returns
    -------
    DataFrame
        'bmi'、'bmr'、および'category_bmi'列が追加されたデータフレームを返します。
    """
    
    df['bmi'] = round(df['weight_kg'] / (df['height_cm']/100)**2, ndigits=2)
    
    men_idx = df[df['gender']=='M'].index.to_list()
    women_idx = df[df['gender']=='F'].index.to_list()
    
    df.loc[men_idx, ['bmr']] = round(66.47 + (13.75 * df[df['gender'] == 'M']['weight_kg']) + (5.003 * df[df['gender']=='M']['height_cm']) - (6.755 * df[df['gender']=='M']['age']), ndigits=2)

    df.loc[women_idx, ['bmr']] = round(655.1 + (9.563 * df[df['gender'] == 'F']['weight_kg']) + (1.85 * df[df['gender']=='F']['height_cm']) - (4.676 * df[df['gender']=='F']['age']), ndigits=2)
    
    
    df['category_bmi'] = df['bmi'].apply(categorize_bmi)
    
    # Calculate body surface area for each row in the data
    df['body_surface_area'] = calculate_bsa(df['height_cm'], df['weight_kg'])