from xgboost import XGBRegressor as XGBR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.linear_model import LinearRegression as LinearR
# from sklearn.datasets import load_boston
from sklearn.model_selection import KFold, cross_val_score as CVS, train_test_split
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from time import time
import datetime
import os
import pickle


class predict_time_ssim(object):
    def __init__(self, file, y_label):
        self.file = file
        self.y_label = y_label

    def load_data(self):
        data = pd.read_csv(self.file)
        cols = ['Scale', 'SampleSet', 'HalfRes', 'Quality', 'GPUFrequency', 'Time', 'SSIM']
        self.data = data[cols]

    def split_train_test(self):
        x = self.data.loc[:, ['Scale', 'SampleSet', 'HalfRes', 'Quality', 'GPUFrequency']]
        y = self.data.loc[:, [self.y_label]]

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    def train_data(self):
        max_depth_list = []
        test_score = []
        train_score = []
        mse_score = []
        mae_score = []
        mae_train_score = []
        mae_all_score = []
        for i in range(1, 30):
            reg = XGBR(n_estimators=100, max_depth=i).fit(self.x_train, self.y_train)  # 交叉验证不要.fit
            max_depth_list.append(i)
            test_score.append(reg.score(self.x_test, self.y_test))
            train_score.append(reg.score(self.x_train, self.y_train))
            mse_score.append(MSE(self.y_test, reg.predict(self.x_test)))
            mae_score.append(MAE(self.y_test, reg.predict(self.x_test)))
            mae_train_score.append(MAE(self.y_train, reg.predict(self.x_train)))
            mae_all_score.append(MAE(pd.concat([self.y_train, self.y_test], axis=0),
                                     pd.concat([pd.Series(reg.predict(self.x_train)), pd.Series(reg.predict(self.x_test))])))
        print('最小的MAE为：' + str(min(mae_all_score)) + ',对应的max_depth为：' + str(mae_all_score.index(min(mae_all_score))))
        self.reg = XGBR(n_estimators=100, max_depth=mae_all_score.index(min(mae_all_score))).fit(self.x_train, self.y_train)

    def output(self):
        y_pred = pd.concat([pd.Series(self.reg.predict(self.x_test)), pd.Series(self.reg.predict(self.x_train))], axis=0)
        data = pd.concat([pd.concat([self.x_test, self.y_test], axis=1), pd.concat([self.x_train, self.y_train], axis=1)], axis=0)
        y_pred = pd.DataFrame(y_pred)
        y_pred = y_pred.reset_index(drop=True)
        data = data.reset_index(drop=True)
        data = pd.concat([data, y_pred], axis=1)
        data.rename({0: 'result_' + self.y_label}, axis=1, inplace=True)
        data.to_excel(self.file.split('.')[0] + self.y_label + '.xlsx', index=False)
        pickle.dump(self.reg, file=open(r'LOD30data_Time.pkl', 'wb+'))

    def main(self):
        self.load_data()
        self.split_train_test()
        self.train_data()
        self.output()


a = predict_time_ssim(file=r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD30data.csv', y_label='Time')
a.main()