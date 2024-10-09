import numpy as np
import pandas as pd
import pickle
'''旧的神经网络用，已废弃'''
# import inference
#
import unreal_engine as ue
def Generate_input(Scale, SampleSet, HalfRes, Quality, GPUFrequency):
    test_data = np.array([Scale, SampleSet, HalfRes, Quality, GPUFrequency])
    # 使用 numpy 的 tile 函数复制数据两次
    test_data = np.tile(test_data, 2)
    return test_data

class calculate:
    def __init__(self):
        self.SSIM_model = None
        self.time_model = None
        self.data = None
        self.SampleSets = [0,1,2]
        self.HalfReses = [0, 1]
        self.Qualitys = [0,1]
        # 初始化空列表
        self.Scale = []
        self.SampleSet = []
        self.HalfRes = []
        self.Quality = []
        self.GPUFrequency = []

        # 遍历所有Scales、SampleSets、HalfReses、Qualitys
        for i in range(1, 20, 1):
            for j in self.SampleSets:
                for k in self.HalfReses:
                    for l in self.Qualitys:
                        self.Scale.append(i/10)
                        self.SampleSet.append(j)
                        self.HalfRes.append(k)
                        self.Quality.append(l)

    def begin_play(self):
        self.uobject.get_owner().bind_event('calculateSet',self.calculateSet)
        self.uobject.get_owner().bind_event('ManualCalculateSet',self.ManualCalculateSet)
        self.uobject.get_owner().bind_event('XGBoostCalculateSet',self.XGBoostcalculateSet)
    def calculateSet(self):
        Actor = self.uobject.get_owner()
        # model = inference.load_model(r"C:\Users\gyp\Desktop\山大渲染组\4S_2023_10_task\作业\第四次附件+代码\第九次改网络GPU频率\SSIM_predict.pth")
        time_model = inference.load_model(r"C:\Users\gyp\Desktop\山大渲染组\4S_2023_10_task\作业\第四次附件+代码\第九次改网络GPU频率\Time_predict.pth")
        quality_model=inference.load_model(r"C:\Users\gyp\Desktop\山大渲染组\4S_2023_10_task\作业\第四次附件+代码\第九次改网络GPU频率\SSIM_predict.pth")
        # 传递一个包含相同数据的一维数组
        
        all_set = []
        time_ok_set = []
        Scales = []  # 0~1.9
        SampleSets = [2, 1, 0]
        HalfReses = [0, 1]
        Qualitys = [1, 0]
        GPUFrequencys = Actor.GPUFrequency # 500~1000
        
        # 假设 Generate_input 在每次迭代中返回一个列表
        for i in range(2, 20, 1):
            for j in SampleSets:
                for k in HalfReses:
                    for l in Qualitys:
                        all_set.append(Generate_input(i / 10, j, k, l, GPUFrequencys/1000))
        
        # 将 all_set 转换为 NumPy 数组
        all_set = np.array(all_set)
        
        # 假设 inference.predict 接受 NumPy 数组作为输入
        time_predictions = inference.predict(time_model, all_set)
        # print(time_predictions)
        
        # A网络根据阈值筛选
        for i in range(len(time_predictions)):
            if time_predictions[i][0] <= 0.5:
                time_ok_set.append(all_set[i])
        
        # 将 time_ok_set 转换为 NumPy 数组
        time_ok_set = np.array(time_ok_set)
        # print(time_ok_set)
        
        # 假设 inference.predict 接受 NumPy 数组作为输入
        SSIM_predictions = inference.predict(quality_model, time_ok_set)
        
        # 找到最大 SSIM 预测值的索引
        max_index = np.argmax(SSIM_predictions[:, 0])
        targetSet=time_ok_set[max_index]
        
        print(time_ok_set[max_index])

        Actor.targetScale=targetSet[0]
        Actor.targetSampleSet=targetSet[1]
        Actor.targetHalfRes=targetSet[2]
        Actor.targetQuality=targetSet[3]
        
        # print("Predictions:")
        # print(predictions)
    def ManualCalculateSet(self):
        data = {
            300: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.7461, 'SSIM': 0.998566622},
            400: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.557667, 'SSIM': 0.999131674},
            500: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.449433, 'SSIM': 0.998462152},
            600: {'Scale': 1.2, 'SampleSet': 0, 'HalfRes': 1, 'Quality': 0, 'Time': 0.321467, 'SSIM': 0.998642376},
            700: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.333767, 'SSIM': 0.998462472},
            800: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.2953, 'SSIM': 0.99855003},
            900: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.268117, 'SSIM': 0.998447722},
            1000: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.240483, 'SSIM': 0.999133007},
            1100: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.218817, 'SSIM': 0.999245993},
            1200: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.203283, 'SSIM': 0.998566624},
            1300: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.1874, 'SSIM': 0.999131623},
            1400: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.172983, 'SSIM': 0.998462446},
            1500: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.163283, 'SSIM': 0.998566646},
            1600: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.15345, 'SSIM': 0.998550368},
            1700: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.144667, 'SSIM': 0.998566633},
            1800: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.1381, 'SSIM': 0.99854458},
            1900: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.131233, 'SSIM': 0.998549972},
            2000: {'Scale': 1.3, 'SampleSet': 0, 'HalfRes': 1, 'Quality': 1, 'Time': 0.10545, 'SSIM': 0.998359663},
            2100: {'Scale': 1.2, 'SampleSet': 0, 'HalfRes': 1, 'Quality': 0, 'Time': 0.1011, 'SSIM': 0.998642382},
            2200: {'Scale': 1.2, 'SampleSet': 0, 'HalfRes': 1, 'Quality': 1, 'Time': 0.096833, 'SSIM': 0.998642117},
            2300: {'Scale': 1.1, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.109933, 'SSIM': 0.998462222},
            2400: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 0, 'Time': 0.106283, 'SSIM': 0.998566645},
            2500: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.101917, 'SSIM': 0.998544332},
            2600: {'Scale': 1.2, 'SampleSet': 1, 'HalfRes': 1, 'Quality': 1, 'Time': 0.0992, 'SSIM': 0.998544079}
        }
        Actor = self.uobject.get_owner()
        GPUFrequency = Actor.GPUFrequencyInt
        Actor.targetScale = data[GPUFrequency]['Scale']
        Actor.targetSampleSet = data[GPUFrequency]['SampleSet']
        Actor.targetHalfRes = data[GPUFrequency]['HalfRes']
        Actor.targetQuality = data[GPUFrequency]['Quality']

    def Generate_input(self, Scale, SampleSet, HalfRes, Quality, GPUFrequency):
        test_data = np.array([Scale, SampleSet, HalfRes, Quality, GPUFrequency])
        return test_data

    def load_models(self, LOD):
        if LOD == 30:
            self.SSIM_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD30data_SSIM.pkl', 'rb'))
            self.time_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD30data_time.pkl', 'rb'))
        elif LOD == 50:
            self.SSIM_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD50data_SSIM.pkl', 'rb'))
            self.time_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD50data_time.pkl', 'rb'))
        elif LOD == 100:
            self.SSIM_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD100data_SSIM.pkl', 'rb'))
            self.time_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD100data_time.pkl', 'rb'))
        else:
            print('没有这个模型！')

    def predict(self, name, data):
        if name == 'SSIM':
            y_pred = pd.DataFrame(self.SSIM_model.predict(data))
        elif name == 'TIME':
            y_pred = pd.DataFrame(self.time_model.predict(data))
        else:
            print("name 错误！")
            return
        self.data = pd.concat([self.data, y_pred], axis=1)
        # self.data.rename({0: 'result_' + self.model.split('_')[1]}, axis=1, inplace=True)
        # self.data.to_excel(r'predict_result.xlsx', index=False)
        # print('输出完毕！')
        return y_pred

    #  LOD=100、50、30 GPUFrequency=300、400...2600
    def XGBoostcalculateSet(self):
        # ue.log("hhhhhhhhhhhhhhhhhhh")
        Actor = self.uobject.get_owner()
        LOD=Actor.SSSLOD
        GPUFrequency=Actor.GPUFrequencyInt
        self.load_models(LOD)  # 加载模型

        # 生成输入数据
        all_set = []
        self.GPUFrequency = []
        # 遍历所有Scales、SampleSets、HalfReses、Qualitys
        for i in range(1, 20, 1):
            for j in self.SampleSets:
                for k in self.HalfReses:
                    for l in self.Qualitys:
                        self.GPUFrequency.append(GPUFrequency)

        all_set = pd.DataFrame([self.Scale, self.SampleSet, self.HalfRes, self.Quality, self.GPUFrequency]).T
        all_set.columns = ['Scale', 'SampleSet', 'HalfRes', 'Quality', 'GPUFrequency']
        time_predictions = self.predict('TIME', all_set)

        # 取time前20%的所有set集合
        threshold_index = int(len(time_predictions.values) * 0.2)
        sorted_indices = sorted(range(len(time_predictions.values)), key=lambda i: time_predictions.values[i])
        min_indices = sorted_indices[:threshold_index]

        time_ok_Scale = [self.Scale[i] for i in min_indices]
        time_ok_SampleSet = [self.SampleSet[i] for i in min_indices]
        time_ok_HalfRes = [self.HalfRes[i] for i in min_indices]
        time_ok_Quality = [self.Quality[i] for i in min_indices]
        time_ok_GPUFrequency = [self.GPUFrequency[i] for i in min_indices]
        time_ok_set = pd.DataFrame(
            [time_ok_Scale, time_ok_SampleSet, time_ok_HalfRes, time_ok_Quality, time_ok_GPUFrequency]).T
        time_ok_set.columns = ['Scale', 'SampleSet', 'HalfRes', 'Quality', 'GPUFrequency']
        SSIM_predictions = self.predict('SSIM', time_ok_set)

        # 找到最大 SSIM 预测值的索引
        max_index = np.argmax(SSIM_predictions.values[:, 0])

        Actor.targetScale =     self.Scale[min_indices[max_index]]
        Actor.targetSampleSet = self.SampleSet[min_indices[max_index]]
        Actor.targetHalfRes =   self.HalfRes[min_indices[max_index]]
        Actor.targetQuality =   self.Quality[min_indices[max_index]]
        print(self.Scale[min_indices[max_index]],
              self.SampleSet[min_indices[max_index]],
              self.HalfRes[min_indices[max_index]],
              self.Quality[min_indices[max_index]],
              self.GPUFrequency[min_indices[max_index]],
              time_predictions.values[min_indices[max_index]],
              SSIM_predictions.values[max_index])
        # ue.log(self.Scale[min_indices[max_index]],
        #       self.SampleSet[min_indices[max_index]],
        #       self.HalfRes[min_indices[max_index]],
        #       self.Quality[min_indices[max_index]],
        #       self.GPUFrequency[min_indices[max_index]],
        #       time_predictions.values[min_indices[max_index]],
        #       SSIM_predictions.values[max_index])




















































#
#
#
#
#
#
#
#
#
#
#
#
#
# import numpy as np
# import pandas as pd
# import pickle
#
#
# class predict_time_ssim(object):
#     def __init__(self):
#         self.SSIM_model = None
#         self.time_model = None
#         self.data = None
#         self.SampleSets = [0,1,2]
#         self.HalfReses = [0, 1]
#         self.Qualitys = [0,1]
#         # 初始化空列表
#         self.Scale = []
#         self.SampleSet = []
#         self.HalfRes = []
#         self.Quality = []
#         self.GPUFrequency = []
#
#         # 遍历所有Scales、SampleSets、HalfReses、Qualitys
#         for i in range(1, 20, 1):
#             for j in self.SampleSets:
#                 for k in self.HalfReses:
#                     for l in self.Qualitys:
#                         self.Scale.append(i/10)
#                         self.SampleSet.append(j)
#                         self.HalfRes.append(k)
#                         self.Quality.append(l)
#
#
#     def Generate_input(self, Scale, SampleSet, HalfRes, Quality, GPUFrequency):
#         test_data = np.array([Scale, SampleSet, HalfRes, Quality, GPUFrequency])
#         return test_data
#
#
#     def load_models(self, LOD):
#         if LOD == 30:
#             self.SSIM_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD30data_SSIM.pkl', 'rb'))
#             self.time_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD30data_time.pkl', 'rb'))
#         elif LOD == 50:
#             self.SSIM_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD50data_SSIM.pkl', 'rb'))
#             self.time_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD50data_time.pkl', 'rb'))
#         elif LOD == 100:
#             self.SSIM_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD100data_SSIM.pkl', 'rb'))
#             self.time_model = pickle.load(open(r'D:\UE4Project\4S_UE\SSS\Content\Scripts\LOD100data_time.pkl', 'rb'))
#         else:
#             print('没有这个模型！')
#
#
#     def predict(self, name, data):
#         if name == 'SSIM':
#             y_pred = pd.DataFrame(self.SSIM_model.predict(data))
#         elif name == 'TIME':
#             y_pred = pd.DataFrame(self.time_model.predict(data))
#         else:
#             print("name 错误！")
#             return
#         self.data = pd.concat([self.data, y_pred], axis=1)
#         # self.data.rename({0: 'result_' + self.model.split('_')[1]}, axis=1, inplace=True)
#         # self.data.to_excel(r'predict_result.xlsx', index=False)
#         # print('输出完毕！')
#         return y_pred
#
#
#     #  LOD=100、50、30 GPUFrequency=300、400...2600
#     def calculateSet(self, LOD, GPUFrequency):
#         self.load_models(LOD)  # 加载模型
#
#         # 生成输入数据
#         all_set = []
#         self.GPUFrequency = []
#         # 遍历所有Scales、SampleSets、HalfReses、Qualitys
#         for i in range(1, 20, 1):
#             for j in self.SampleSets:
#                 for k in self.HalfReses:
#                     for l in self.Qualitys:
#                         self.GPUFrequency.append(GPUFrequency)
#
#         all_set = pd.DataFrame([self.Scale, self.SampleSet, self.HalfRes, self.Quality, self.GPUFrequency]).T
#         all_set.columns = ['Scale', 'SampleSet', 'HalfRes', 'Quality', 'GPUFrequency']
#         time_predictions = self.predict('TIME', all_set)
#
#         # 取time前20%的所有set集合
#         threshold_index = int(len(time_predictions.values) * 0.2)
#         sorted_indices = sorted(range(len(time_predictions.values)), key=lambda i: time_predictions.values[i])
#         min_indices = sorted_indices[:threshold_index]
#
#
#         time_ok_Scale =     [self.Scale[i] for i in min_indices]
#         time_ok_SampleSet = [self.SampleSet[i] for i in min_indices]
#         time_ok_HalfRes =   [self.HalfRes[i] for i in min_indices]
#         time_ok_Quality =   [self.Quality[i] for i in min_indices]
#         time_ok_GPUFrequency = [self.GPUFrequency[i] for i in min_indices]
#         time_ok_set = pd.DataFrame([time_ok_Scale, time_ok_SampleSet, time_ok_HalfRes, time_ok_Quality, time_ok_GPUFrequency]).T
#         time_ok_set.columns = ['Scale', 'SampleSet', 'HalfRes', 'Quality', 'GPUFrequency']
#         SSIM_predictions = self.predict('SSIM', time_ok_set)
#
#         # 找到最大 SSIM 预测值的索引
#         max_index = np.argmax(SSIM_predictions.values[:, 0])
#
#         print(self.Scale[min_indices[max_index]],
#               self.SampleSet[min_indices[max_index]],
#               self.HalfRes[min_indices[max_index]],
#               self.Quality[min_indices[max_index]],
#               self.GPUFrequency[min_indices[max_index]],
#               time_predictions.values[min_indices[max_index]],
#               SSIM_predictions.values[max_index])
#
#
# a = predict_time_ssim()
# LOD_values = [100, 50, 30]
# GPUFrequency_values = list(range(300, 2601, 100))
# for LOD in LOD_values:
#     print("LOD:", LOD)
#     for GPUFrequency in GPUFrequency_values:
#         a.calculateSet(LOD, GPUFrequency)
# ue.log("hhhhhhhhhhhhhhhhhhh")