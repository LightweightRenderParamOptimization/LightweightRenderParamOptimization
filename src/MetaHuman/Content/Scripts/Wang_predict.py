import numpy as np
import pandas as pd
import pickle
import torch
import time
import sys
import torch.nn as nn
import torch.nn.functional as F

# sys.path.append(r'D:\bad_thing\graduate0\low cost render\deep_learning_for_cv-master\1_classification\c02_MLP\model\wangs_qual')
# from network_qual import PredictiveModel as q_model
# import network_qual
# sys.path.append(r'D:\bad_thing\graduate0\low cost render\deep_learning_for_cv-master\1_classification\c02_MLP\model\wangs_time')
# from network_time import PredictiveModel as t_model
'''旧的神经网络用，已废弃'''
# import inference
#
import unreal_engine as ue


class TimeModel(nn.Module):
    def __init__(self):
        super(TimeModel, self).__init__()
        self.fc1 = nn.Linear(5, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 8)
        self.fc5 = nn.Linear(8, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x


class QualModel(nn.Module):
    def __init__(self):
        super(QualModel, self).__init__()
        self.fc1 = nn.Linear(5, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 8)
        self.fc5 = nn.Linear(8, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x


class calculate:

    def __init__(self):
        self.SSIM_model = QualModel()
        self.SSIM_model.load_state_dict(torch.load(r"D:\UE4Project\MetaHuman\Content\Scripts\Wangsss_qual_model.pth"))
        self.SSIM_model.eval()
        self.time_model = TimeModel()
        self.time_model.load_state_dict(torch.load(r"D:\UE4Project\MetaHuman\Content\Scripts\Wangsss_time_model.pth"))
        self.time_model.eval()
        self.data = None

        self.SampleSets = [0, 1, 2]
        self.HalfReses = [0, 1]
        self.Qualitys = [0, 1]
        # 初始化空列表
        self.Scale = []
        self.SampleSet = []
        self.HalfRes = []
        self.Quality = []
        self.GPUFrequency = []

        # self.SSAOIntes = [0.2, 0.6, 1.0]
        # self.SSAOBias = [1, 0.5, 0]
        # self.SSAOQuals = [0.2, 0.6, 1.0]
        # self.RTAOIntes = [0.2, 0.6, 1.0]
        # self.RTAOSSTs = [1, 2, 4]
        # # 初始化空列表
        # self.SSAOInte = []
        # self.SSAOBia = []
        # self.SSAOQual = []
        # self.RTAOInte = []
        # self.RTAOSST = []
        # self.GPUFrequency = []

        # 遍历所有Scales、SampleSets、HalfReses、Qualitys
        for i in range(1, 20, 1):
            for j in self.SampleSets:
                for k in self.HalfReses:
                    for l in self.Qualitys:
                        self.Scale.append(i / 10)
                        self.SampleSet.append(j)
                        self.HalfRes.append(k)
                        self.Quality.append(l)

    def begin_play(self):
        self.uobject.get_owner().bind_event('WangPredict', self.WangPredict)

    def Generate_input(self, Scale, SampleSet, HalfRes, Quality, GPUFrequency):
        test_data = np.column_stack((Scale, SampleSet, HalfRes, Quality, GPUFrequency))
        test_data = torch.Tensor(test_data)
        return test_data

    def predict(self, name, data):
        print(data.shape)
        if name == 'SSIM':
            with torch.no_grad():
                predictions = self.SSIM_model(data)
        elif name == 'TIME':
            with torch.no_grad():
                predictions = self.time_model(data)
        else:
            print("name 错误！")
            return
        # predictions = pd.DataFrame(predictions.numpy())

        # 确保self.data是一个DataFrame并且与predictions具有相同的行数
        # if not isinstance(self.data, pd.DataFrame) or len(self.data) != len(predictions):
        #     print("self.data必须是一个pandas DataFrame，并且行数要与predictions相同。")
        #     return

        # # 沿着列的方向拼接数据
        # self.data = pd.concat([self.data, predictions], axis=1)

        return predictions

    #  LOD=100、50、30 GPUFrequency=300、400...2600
    def WangPredict(self):
        # ue.log("hhhhhhhhhhhhhhhhhhh")

        start_time = time.time()

        Actor = self.uobject.get_owner()
        # LOD=Actor.SSSLOD
        GPUFrequency = Actor.GPUFrequencyInt
        # self.load_models(LOD)  # 加载模型

        # 生成输入数据
        all_set = []
        self.GPUFrequency = []

        self.GPUFrequency = [GPUFrequency] * 228

        all_set = self.Generate_input(self.Scale, self.SampleSet, self.HalfRes, self.Quality, self.GPUFrequency)
        time_predictions = self.predict('TIME', all_set)

        time_predictions = time_predictions.squeeze(1)
        threshold_index = int(time_predictions.size(0) * 0.2)
        values, min_indices = torch.topk(-time_predictions, threshold_index)
        min_indices = min_indices[:threshold_index]
        time_ok_Scale = [self.Scale[i] for i in min_indices]
        time_ok_SampleSet = [self.SampleSet[i] for i in min_indices]
        time_ok_HalfRes = [self.HalfRes[i] for i in min_indices]
        time_ok_Quality = [self.Quality[i] for i in min_indices]
        time_ok_GPUFrequency = [self.GPUFrequency[i] for i in min_indices]

        # time_ok_SSAOInte = [self.SSAOInte[i] for i in min_indices]
        # time_ok_SSAOBia = [self.SSAOBia[i] for i in min_indices]
        # time_ok_SSAOQual = [self.SSAOQual[i] for i in min_indices]
        # time_ok_RTAOInte = [self.RTAOInte[i] for i in min_indices]
        # time_ok_RTAOSST = [self.RTAOSST[i] for i in min_indices]
        time_ok_set = self.Generate_input(time_ok_Scale, time_ok_SampleSet, time_ok_HalfRes, time_ok_Quality,
                                          time_ok_GPUFrequency)
        SSIM_predictions = self.predict('SSIM', time_ok_set)
        max_index = np.argmax(SSIM_predictions[:, 0])
        SSIM_predictions = SSIM_predictions.squeeze(1)

        Actor.targetScale = self.Scale[min_indices[max_index]]
        Actor.targetSampleSet = self.SampleSet[min_indices[max_index]]
        Actor.targetHalfRes = self.HalfRes[min_indices[max_index]]
        Actor.targetQuality = self.Quality[min_indices[max_index]]

        end_time = time.time()
        print("time:", end_time - start_time)
        print(self.Scale[min_indices[max_index]],
              self.SampleSet[min_indices[max_index]],
              self.HalfRes[min_indices[max_index]],
              self.Quality[min_indices[max_index]],

              self.GPUFrequency[min_indices[max_index]],
              time_predictions[min_indices[max_index]].item(),
              SSIM_predictions[max_index].item())

        # ue.log(self.Scale[min_indices[max_index]],
        #       self.SampleSet[min_indices[max_index]],
        #       self.HalfRes[min_indices[max_index]],
        #       self.Quality[min_indices[max_index]],
        #       self.GPUFrequency[min_indices[max_index]],
        #       time_predictions.values[min_indices[max_index]],
        #       SSIM_predictions.values[max_index])