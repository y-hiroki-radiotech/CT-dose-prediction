from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
import pandas as pd


# Making the ModelTraining class independent of FeatureEngineering

class IndependentModelTraining:

    def __init__(self):
        self.pitch_factor_model = None
        self.exposure_time_model = None

    def train_pitch_factor_model(self, df):
        columns = ['bmi', 'body_surface_area']
        X = df.loc[:, columns]
        y = df['pitch factor'].astype('str')
        
        self.pitch_factor_model = DecisionTreeClassifier(criterion='entropy', max_depth=8, random_state=42)
        self.pitch_factor_model.fit(X, y)

    def train_exposure_time_model(self, df):
        columns = ['bmi', 'body_surface_area']
        X = df.loc[:, columns]
        y = df['exposure time'].astype('str')
        
        self.exposure_time_model = DecisionTreeClassifier(criterion='entropy', max_depth=8, random_state=42)
        self.exposure_time_model.fit(X, y)

    def predict_pitch_factor(self, df):
        if self.pitch_factor_model:
            columns = ['bmi', 'body_surface_area']
            X = df.loc[:, columns]
            predictions = self.pitch_factor_model.predict(X)
            return predictions
        else:
            raise ValueError("Pitch factor model is not trained yet.")

    def predict_exposure_time(self, df):
        if self.exposure_time_model:
            columns = ['bmi', 'body_surface_area']
            X = df.loc[:, columns]
            predictions = self.exposure_time_model.predict(X)
            return predictions
        else:
            raise ValueError("Exposure time model is not trained yet.")


# Updating the data preprocessing function to keep all columns

class PitchRotationTimeModel(IndependentModelTraining):

    def load_and_preprocess_data(self, df_input):
        df = df_input.copy()
        
        scan_areas = [
            '胸部CT', '胸部〜骨盤CT', '腹部〜骨盤CT', '副鼻腔CT', '胸腰椎CT', '大腿・膝・下腿CT',
            '上腹部CT', '体幹部Dual Energy CT', '足・足関節CT', '肩・上腕・鎖骨CT', '頸部〜骨盤CT', 
            '肘・前腕・手関節CT', '頸椎・頚髄CT', '頸部CT', '骨盤骨CT', '顔面骨CT', '冠動脈CT', 
            '肺静脈CT', '肺塞栓CT', '歯・顎骨CT', '脳Perfusion', '脳CTA', '脳CT'
        ]
        
        df_dict = {scan_area: df[df['scan_area'] == scan_area] for scan_area in scan_areas}
        
        return df_dict

    def fit(self, df_train_input):
        # Load and preprocess data
        df_dict = self.load_and_preprocess_data(df_train_input)
        
        # Combine the dataframes for model training
        df_train = pd.concat(df_dict.values(), axis=0)
        
        # Train the models
        self.train_pitch_factor_model(df_train)
        self.train_exposure_time_model(df_train)
        
        # Predict using the trained models on training data
        for key, df in df_dict.items():
            df['predicted_pitch_factor'] = self.predict_pitch_factor(df)
            df['predicted_exposure_time'] = self.predict_exposure_time(df)
        
        # Combine the dataframes for output
        df_train_transformed = pd.concat(df_dict.values(), axis=0)
        
        return df_train_transformed

    def transform(self, df_input):
        # Load and preprocess data
        df_dict = self.load_and_preprocess_data(df_input)
        
        predicted_df_dict = {}
        
        # Predict using the trained models and create a new dataframe for predictions
        for key, df in df_dict.items():
            new_df = df.copy()
            new_df['predicted_pitch_factor'] = self.predict_pitch_factor(df)
            new_df['predicted_exposure_time'] = self.predict_exposure_time(df)
            predicted_df_dict[key] = new_df

        # Combine the new dataframes for output
        df_transformed = pd.concat(predicted_df_dict.values(), axis=0)
        return df_transformed
if __name__ == '__main__':
    # Testing the updated class again

    model_trainer_v3 = FinalModelTrainingV3()
    model_trainer_v3.fit("/mnt/data/modify_preprocess_train_data.xlsx")
    transformed_data_v3 =model_trainer_v3.transform("/mnt/data/modify_preprocess_train_data.xlsx")
    transformed_data_v3.head()
