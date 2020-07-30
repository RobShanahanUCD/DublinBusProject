import pandas as pd
import numpy as np

import lightgbm as lgb
import joblib
from sklearn.model_selection import cross_val_score
from bus_stops.ml_models.all_route import RouteList


class ModelTraining:
    """Training all the models for all routes"""

    def route_time_process(self, df):
        df['hour'] = (df['ActualTime_Arr'] // 3600) % 24
        return df

    def convert_2_datetime(self, df, col):
        df[col] = pd.to_datetime(df[col])
        return df

    def add_bank_holiday(self, df, col, bank_holidays, date_col):
        df['bank_holiday'] = np.where(df[col].astype(str).isin(set(list(bank_holidays[date_col].astype(str)))), 1, 0)
        return df

    def merge_and_clean(self, df1, df2, col):
        combined_df = pd.merge(df1, df2, how='inner', left_on=['DayOfService', 'hour'],
                               right_on=['date', 'hour'],
                               suffixes=('_route', '_weather'))
        combined_df['Direction'] = combined_df['Direction'].astype('int')
        combined_df['day_of_week'] = combined_df['DayOfService'].dt.dayofweek
        combined_df['day_of_year'] = combined_df['DayOfService'].dt.dayofyear
        combined_df['journey_time'] = combined_df['ActualTime_Dep'] - combined_df['PlannedTime_Arr']
        combined_df['journey_time'] = combined_df['journey_time'].apply(lambda x: x if x > 0 else 0)
        combined_df['StopPointID'] = combined_df['StopPointID'].astype('category')
        combined_df = combined_df[col]
        return combined_df

    def remove_outlier(self, df):
        df = df[np.abs(df["journey_time"] - df["journey_time"].mean( )) <= (1.5 * df["journey_time"].std( ))]
        return df

    def time_transform(self, df, col, max_val):
        """Sine-cosine encoding to extract the cyclic property of time"""
        df[col + '_sin'] = np.sin(2 * np.pi * df[col] / max_val)
        df[col + '_cos'] = np.cos(2 * np.pi * df[col] / max_val)
        df = df.drop([col], axis=1)
        return df

    def train(self, route_path):
        route = pd.read_pickle(route_path)
        bank_holidays = pd.read_pickle("../../../DataAnalytics/bank_holidays__.pkl")
        weather = pd.read_pickle("../../../DataAnalytics/weather__.pkl")

        route = self.route_time_process(route)

        route = self.convert_2_datetime(route, 'DayOfService')
        bank_holidays = self.convert_2_datetime(bank_holidays, 'date')
        weather = self.convert_2_datetime(weather, 'date')

        route = self.add_bank_holiday(route, 'DayOfService', bank_holidays, 'date')

        col = ['ProgrNumber', 'Direction', 'hour', 'StopPointID',
               'bank_holiday', 'temp', 'day_of_week', 'day_of_year', 'journey_time']

        df = self.merge_and_clean(route, weather, col)

        df = self.remove_outlier(df)
        df = self.time_transform(df, 'day_of_week', 7)
        df = self.time_transform(df, 'hour', 24)

        y = df['journey_time']
        x = df.loc[:, df.columns != 'journey_time']
        x_train, y_train = x, y

        lgb_turned = lgb.LGBMRegressor( )
        lgb_turned.fit(x_train, y_train)
        scores = cross_val_score(lgb_turned, x_train, y_train, scoring='neg_mean_absolute_error', cv=5)
        avg_score = np.mean(scores)
        avg_journey_time = y_train.mean( )
        error_rate = -avg_score * 100 / avg_journey_time
        print("avg_journey_time: ", avg_journey_time)
        print("Score:", scores)
        print("- MAE: {:.5f}".format(avg_score), ";   Error rate: ", -avg_score * 100 / avg_journey_time, "%")

        model_name = route_path.split(".")[0] + 'lgbm_model.pkl'
        joblib.dump(lgb_turned, model_name)
        log_row = {"model": route_path, "mae": avg_score,
                   "avg_journey_time": avg_journey_time,
                   "error_rate": error_rate, "scores": scores}

        print(model_name, " Training Success!")
        return log_row


if __name__ == '__main__':
    route_list = RouteList( ).route_list
    route_list = ["route_" + route + "__.pkl" for route in route_list]
    print(route_list)

    log = pd.DataFrame(columns=["model", "mae", "avg_journey_time", "error_rate", "scores"])
    for route_path in route_list:
        print(route_path)
        # if os.path.isfile('./' + route_path.split(".")[0] + 'lgbm_model.pkl'):
        #     continue
        log = log.append(ModelTraining( ).train(route_path), ignore_index=True)
        log.to_csv("training_log.csv", index=False)
