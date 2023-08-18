import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans



class FeatureEngineering:
    
    def __init__(self):
        self.bmi_bsa_scaler = None
        self.age_weight_scaler = None
        self.bmi_bsa_kmeans = None
        self.age_weight_kmeans = None
        
    @staticmethod
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
    
    @staticmethod
    def calculate_bsa(height_cm, weight_kg):
        bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)
        return bsa
    
    
    def fit(self, df_train):
        # Calculating bmi and bsa for train data
        df_train['bmi'] = round(df_train['weight_kg'] / (df_train['height_cm']/100)**2, ndigits=2)
        df_train['body_surface_area'] = self.calculate_bsa(df_train['height_cm'], df_train['weight_kg'])
        
        # Fit the KMeans and scalers using the train data
        self.bmi_bsa_scaler = StandardScaler()
        self.bmi_bsa_scaler.fit(df_train[['bmi', 'body_surface_area']])
        
        self.age_weight_scaler = StandardScaler()
        self.age_weight_scaler.fit(df_train[['age', 'weight_kg']])
        
        # BMI and BSA clustering
        X_train_bmi_bsa = self.bmi_bsa_scaler.transform(df_train[['bmi', 'body_surface_area']])
        self.bmi_bsa_kmeans = KMeans(n_clusters=9, random_state=42)
        self.bmi_bsa_kmeans.fit(X_train_bmi_bsa)
        
        # Age and weight clustering
        X_train_age_weight = self.age_weight_scaler.transform(df_train[['age', 'weight_kg']])
        self.age_weight_kmeans = KMeans(n_clusters=10, random_state=42)
        self.age_weight_kmeans.fit(X_train_age_weight)
        
        
    def transform(self, df):
        # Calculating bmi, bmr, bsa
        df['bmi'] = round(df['weight_kg'] / (df['height_cm']/100)**2, ndigits=2)
        men_idx = df[df['gender']=='M'].index.to_list()
        women_idx = df[df['gender']=='F'].index.to_list()
        df.loc[men_idx, ['bmr']] = round(66.47 + (13.75 * df[df['gender'] == 'M']['weight_kg']) + (5.003 * df[df['gender']=='M']['height_cm']) - (6.755 * df[df['gender']=='M']['age']), ndigits=2)
        df.loc[women_idx, ['bmr']] = round(655.1 + (9.563 * df[df['gender'] == 'F']['weight_kg']) + (1.85 * df[df['gender']=='F']['height_cm']) - (4.676 * df[df['gender']=='F']['age']), ndigits=2)
        df['category_bmi'] = df['bmi'].apply(self.categorize_bmi)
        df['body_surface_area'] = self.calculate_bsa(df['height_cm'], df['weight_kg'])
        
        
        # Age era
        df['age_era'] = (df['age'] // 10) * 10
        
        # KMeans transformations
        X_bmi_bsa = self.bmi_bsa_scaler.transform(df[['bmi', 'body_surface_area']])
        df['bmi_body_surface_area_category'] = self.bmi_bsa_kmeans.predict(X_bmi_bsa)
        
        X_age_weight = self.age_weight_scaler.transform(df[['age', 'weight_kg']])
        df['age_weight_kg_category'] = self.age_weight_kmeans.predict(X_age_weight)
        
        
        # Combine features
        df['scan_area_method_combine'] = df['scan_area'] + '_' + df['scan_method']
        df['scan_area_method_bmi_catgory_combine'] = df['scan_area'] + '_' + df['scan_method']  + '_' + df['category_bmi']
        df['bmi_bsa_cat_scan_area_method_combine'] = df['bmi_body_surface_area_category'].astype(str) + df['scan_area_method_combine']
        df['age_weight_cat_scan_area_method_combine'] = df['age_weight_kg_category'].astype(str) + df['scan_area_method_combine']
        
        
        return df
        