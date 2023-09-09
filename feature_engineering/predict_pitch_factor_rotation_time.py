import pandas as pd
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier


class CTDataProcessor:
    def __init__(self, df_train):
        self.df = df_train

    def replace_pitch_factor(self):
        def replace_func(df):
            if df['pitch factor'] == 0.99 or df['pitch factor'] == 0.98:
                return 1.0
            elif df['pitch factor'] == 0.52:
                return 0.51
            else:
                return df['pitch factor']

        self.df['pitch factor'] = self.df.apply(replace_func, axis=1)

    def split_by_scan_area(self, area):
        self.df_list = self.df[self.df['scan_area'] == area]


class CTPitchRotation:
    def __init__(self, df_train, df_test):
        self.df_train = df_train
        self.df_test = df_test

    def classify_rotation_exposure_time(self):
        columns = ['bmi', 'body_surface_area']
        # Training for exposure time
        X = self.df_train.loc[:, columns]
        y = self.df_train['exposure time per rotation'].astype('str')
        tree_model_exposure = DecisionTreeRegressor(criterion='absolute_error', max_depth=4, random_state=42)
        tree_model_exposure.fit(X, y)

        # Test for exposure time
        X_test = df_test.loc[:, columns]
        y_pred_exposure_time = tree_model_exposure.predict(X_test.loc[:, columns])
        self.df_test['predicted_exposure_time'] = y_pred_exposure_time

        # Training for pitch factor
        y = self.df_train['pitch factor'].astype('str')
        tree_model_pitch = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=42)
        tree_model_pitch.fit(X, y)

        # Test for pitch factore
        y_pred_pitch = tree_model_pitch.predict(X_test.loc[:, columns])
        self.df_test['predicted_pitch_factor'] = y_pred_pitch


if __name__ == '__main__':
    df = pd.read_excel('preprocessed_train_data.xlsx')
    fe = FeatureEngineering()
    fe.fit(df)
    df_train_transformed = fe.transform(df)

    data_processor = CTDataProcessor(df_train_transformed)
    data_processor.replace_pitch_factor()
    data_processor.split_by_scan_area('脳CT')

    pitch_rotation_model = CTPitchRotationTrain(data_processor.df_list, df_test)