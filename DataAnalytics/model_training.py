import pandas as pd
import numpy as np

import lightgbm as lgb
import joblib
from sklearn.model_selection import cross_val_score


def train(route_path):
    def route_time_process(df):
        df['hour'] = (df['ActualTime_Arr'] // 3600) % 24
        return df

    def convert_2_datetime(df, col):
        df[col] = pd.to_datetime(df[col])
        return df

    def add_bank_holiday(df, col, bank_holidays, date_col):
        df['bank_holiday'] = np.where(df[col].astype(str).isin(set(list(bank_holidays[date_col].astype(str)))), 1, 0)
        return df

    def merge_and_clean(df1, df2, col):
        combined_df = pd.merge(df1, df2, how='inner', left_on=['DayOfService', 'hour'],
                               right_on=['date', 'hour'],
                               suffixes=('_route', '_weather'))
        combined_df['Direction'] = combined_df['Direction'].astype('int')
        combined_df['day_of_week'] = combined_df['DayOfService'].dt.dayofweek
        combined_df['day_of_year'] = combined_df['DayOfService'].dt.dayofyear
        combined_df['journey_time'] = combined_df['ActualTime_Dep'] - combined_df['PlannedTime_Arr']
        combined_df['journey_time'] = combined_df['journey_time'].apply(lambda x: x if x > 0 else 0)
        combined_df = combined_df[col]
        return combined_df

    def remove_outlier(df):
        df = df[np.abs(df["journey_time"] - df["journey_time"].mean( )) <= (1 * df["journey_time"].std( ))]
        return df

    def time_transform(df, col, max_val):
        df[col + '_sin'] = np.sin(2 * np.pi * df[col] / max_val)
        df[col + '_cos'] = np.cos(2 * np.pi * df[col] / max_val)
        df = df.drop([col], axis=1)
        return df

    route = pd.read_pickle(route_path)
    bank_holidays = pd.read_pickle("./bank_holidays__.pkl")
    weather = pd.read_pickle("./weather__.pkl")

    route = route_time_process(route)

    route = convert_2_datetime(route, 'DayOfService')
    bank_holidays = convert_2_datetime(bank_holidays, 'date')
    weather = convert_2_datetime(weather, 'date')

    route = add_bank_holiday(route, 'DayOfService', bank_holidays, 'date')

    col = ['ProgrNumber', 'Direction', 'hour',
           'bank_holiday', 'temp', 'day_of_week', 'day_of_year', 'journey_time']

    df = merge_and_clean(route, weather, col)

    df = remove_outlier(df)
    df = time_transform(df, 'day_of_week', 7)
    df = time_transform(df, 'hour', 24)

    y = df['journey_time']
    x = df.loc[:, df.columns != 'journey_time']
    x_train, y_train = x, y

    lgb_turned = lgb.LGBMRegressor()
    lgb_turned.fit(x_train, y_train)
    scores = cross_val_score(lgb_turned, x_train, y_train, scoring='neg_root_mean_squared_error', cv=5)
    print("- RMSE: {:.5f}".format(np.mean(scores)))

    model_name = route_path.split(".")[0] + 'lgbm_model.pkl'
    joblib.dump(lgb_turned, model_name)

    print(model_name, " Training Success!")


if __name__ == '__main__':
    routes = [
        'route_14__.pkl',
        'route_63__.pkl',
        'route_79A__.pkl',
    ]

    for route_path in routes:
        train(route_path)
