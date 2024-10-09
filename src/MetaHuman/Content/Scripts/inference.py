import torch
import pandas as pd
from network import CustomNetwork

def load_data(file_path):
    data = pd.read_csv(file_path, sep=',')
    test_data = data.iloc[:, 1:11].values
    test_result = data.iloc[:, 12].values
    return test_data, test_result

def load_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CustomNetwork().to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def predict(model, test_data):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs1 = torch.tensor(test_data[:,0:5], dtype=torch.float32).to(device)
    inputs2 = torch.tensor(test_data[:,5:10], dtype=torch.float32).to(device)
    with torch.no_grad():
        outputs = model(inputs1, inputs2)
    predictions = outputs.cpu().numpy()
    return predictions

def main():
    test_data, test_result = load_data(r"C:\Users\gyp\Desktop\山大渲染组\4S_2023_10_task\作业\第四次附件+代码\第九次改网络GPU频率\数据\trainData.csv")
    # model = load_model(r"C:\Users\gyp\Desktop\山大渲染组\4S_2023_10_task\作业\第四次附件+代码\第九次改网络GPU频率\SSIM_predict.pth")
    model = load_model(r"C:\Users\gyp\Desktop\山大渲染组\4S_2023_10_task\作业\第四次附件+代码\第九次改网络GPU频率\Time_predict.pth")
    predictions = predict(model, test_data)
    print("Predictions:")
    print(predictions)
    error = 0
    for i in range(len(predictions)):
        error += abs(predictions[i][0] - test_result[i])
        print(f"Prediction: {predictions[i][0]:.4f}, Actual: {test_result[i]:.4f}, Error: {abs(predictions[i][0] - test_result[i]):.4f}")
    error = error / len(predictions)
    print(f"Average Error: {error:.4f}")

if __name__ == '__main__':
    main()