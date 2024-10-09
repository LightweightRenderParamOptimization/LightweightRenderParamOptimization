#include "GPUFrequencyLibrary.h"

#include "GenericPlatform/GenericPlatformDriver.h"
#include "Runtime/Core/Public/GenericPlatform/GenericPlatformMisc.h"
#include "Stats/StatsData.h"
#include "GameFramework/Actor.h"
#include "Components/StaticMeshComponent.h"
#include "HAL/PlatformProcess.h"
#include "Camera/CameraComponent.h"
#include "Kismet/GameplayStatics.h"
struct FGameThreadStatsData;
/**
// #include "CUDA/Source"
// NvPhysicalGpuHandle UGPUFrequencyLibrary::m_GpuHandle = nullptr;
//
// float UGPUFrequencyLibrary::GetGPUClockFrequency()
// {
//     // 初始化GPU句柄和NVAPI
//     if (!m_GpuHandle)
//     {
//         if (!Init())
//         {
//             // 初始化失败
//             UE_LOG(LogTemp, Error, TEXT("Failed to initialize GPU or NVAPI."));
//             return -1.0f;
//         }
//     }
//
//     // 获取GPU核心时钟频率
//     FrequencyInfo Info;
//     if (GetCoreClockMhz(&Info))
//     {
//         // 成功获取时钟频率
//         return static_cast<float>(Info.NvGraphicsClockInMhz);
//     }
//     else
//     {
//         // 获取失败
//         UE_LOG(LogTemp, Error, TEXT("Failed to get GPU core clock frequency."));
//         return -1.0f;
//     }
// }
//
// bool UGPUFrequencyLibrary::Init()
// {
//     NvAPI_Status Status = NvAPI_Initialize();
//     if (Status != NVAPI_OK)
//     {
//         // 处理初始化失败的情况
//         UE_LOG(LogTemp, Error, TEXT("Failed to initialize NVAPI. Error code: %d"), Status);
//         return false;
//     }
//
//     // 获取物理 GPU 句柄
//     NvPhysicalGpuHandle gpuHandles[NVAPI_MAX_PHYSICAL_GPUS] = { 0 };
//     NvU32 gpuCount = 0;
//     Status = NvAPI_EnumPhysicalGPUs(gpuHandles, &gpuCount);
//
//     // 检查调试信息并根据需要重新获取 GPU 句柄
//     if (Status != NVAPI_OK || gpuCount == 0 ) {
//         UE_LOG(LogTemp, Error, TEXT("Failed to enumerate physical GPUs. Error code: %d"), Status);
//     
//         if (Status == NVAPI_NO_IMPLEMENTATION) {
//             UE_LOG(LogTemp, Error, TEXT("Function not implemented in current driver installation."));
//         }
//
//         NvAPI_Unload();
//         return false;
//     }
//
//     m_GpuHandle = gpuHandles[0];
//     return true;
// }
//
// bool UGPUFrequencyLibrary::GetCoreClockMhz(FrequencyInfo* pInfo)
// {
//     NV_GPU_CLOCK_FREQUENCIES table = { 0 };
//     table.version = NV_GPU_CLOCK_FREQUENCIES_VER;
//     table.ClockType = NV_GPU_CLOCK_FREQUENCIES_CURRENT_FREQ;
//
//     NvAPI_Status Status = NvAPI_GPU_GetAllClockFrequencies(m_GpuHandle, &table);
//     if (Status != NVAPI_OK)
//     {
//         // 处理获取时钟频率失败的情况
//         UE_LOG(LogTemp, Error, TEXT("Failed to get GPU clock frequencies. Error code: %d"), Status);
//         return false;
//     }
//
//     if (!table.domain[NVAPI_GPU_PUBLIC_CLOCK_GRAPHICS].bIsPresent)
//     {
//         // 处理时钟频率不可用的情况
//         UE_LOG(LogTemp, Error, TEXT("GPU graphics clock frequency not present."));
//         return false;
//     }
//
//     NvU32 GraphicsClockInKhz = table.domain[NVAPI_GPU_PUBLIC_CLOCK_GRAPHICS].frequency;
//     pInfo->NvGraphicsClockInMhz = NvU32((GraphicsClockInKhz + 500) / 1000);
//     return true;
// }
// void UGPUFrequencyLibrary::TestGPU()
// {
//     // 初始化 NVAPI
//     NvAPI_Status status = NvAPI_Initialize();
//     if (status != NVAPI_OK) {
//         UE_LOG(LogTemp, Error, TEXT("Failed to initialize NVAPI. Error code: %d"), status);
//         return;
//     }
//
//     // 获取物理 GPU 句柄
//     NvPhysicalGpuHandle gpuHandles[NVAPI_MAX_PHYSICAL_GPUS] = { 0 };
//     NvU32 gpuCount = 0;
//     status = NvAPI_EnumPhysicalGPUs(gpuHandles, &gpuCount);
//     if (status != NVAPI_OK || gpuCount == 0) {
//         UE_LOG(LogTemp, Error, TEXT("111Failed to initialize NVAPI. Error code: %d"), status);
//         NvAPI_Unload();
//         return;
//     }
//
//     // 输出显卡信息
//     for (NvU32 i = 0; i < gpuCount; ++i) {
//         NvAPI_ShortString gpuName;
//         status = NvAPI_GPU_GetFullName(gpuHandles[i], gpuName);
//         if (status == NVAPI_OK) {
//             UE_LOG(LogTemp, Error, TEXT("GPU %d: %s"), i + 1, gpuName);
//         } else {
//             UE_LOG(LogTemp, Error, TEXT("Failed to get GPU name. Error code: %d"), status);
//         }
//     }
//
//     // 卸载 NVAPI
//     NvAPI_Unload();
// }
// float UGPUFrequencyLibrary::GetGPUClockFrequency()
// {
// 	
// 	// 获取GPU信息
// 	const FGPUDriverInfo* GPUDriverInfo = FGenericPlatformMisc::GetGPUDriverInfo();
//
// 	if (GPUDriverInfo)
// 	{
// 		// 输出GPU信息，包括工作频率
// 		UE_LOG(LogTemp, Warning, TEXT("GPU Name: %s"), *GPUDriverInfo->GetName());
// 		UE_LOG(LogTemp, Warning, TEXT("  Clock Rate: %f MHz"), GPUDriverInfo-> / 1000.0f);
// 	}
// 	else
// 	{
// 		UE_LOG(LogTemp, Error, TEXT("Failed to get GPU information."));
// 	}
// }
**/
UGPUFrequencyLibrary::UGPUFrequencyLibrary()
{
	// 初始化 NVML 库
	nvmlReturn_t result = nvmlInit();
	if (result != NVML_SUCCESS) {
		UE_LOG(LogTemp, Error, TEXT("Failed to initialize NVML: %s"), *FString(nvmlErrorString(result)));
	}
}

UGPUFrequencyLibrary::~UGPUFrequencyLibrary()
{
	
	// 关闭 NVML 库
	nvmlShutdown();
}

float UGPUFrequencyLibrary::GetGPUClockFrequency()
{
	nvmlReturn_t result;

	// 获取设备数量
	unsigned int deviceCount;
	result = nvmlDeviceGetCount(&deviceCount);
	if (result != NVML_SUCCESS) {
		UE_LOG(LogTemp, Error, TEXT("Failed to get device count: %s"), *FString(nvmlErrorString(result)));
		return 0.0f;
	}

	// 默认选择第一个 GPU
	int targetDeviceIndex = 0;

	// 获取设备句柄
	nvmlDevice_t device;
	result = nvmlDeviceGetHandleByIndex(targetDeviceIndex, &device);
	if (result != NVML_SUCCESS) {
		UE_LOG(LogTemp, Error, TEXT("Failed to get device handle: %s"), *FString(nvmlErrorString(result)));
		return 0.0f;
	}

	// 获取当前 GPU 时钟频率信息
	nvmlClockType_t clockType = NVML_CLOCK_GRAPHICS;  // 图形时钟域
	unsigned int clock;
	result = nvmlDeviceGetClockInfo(device, clockType, &clock);
	if (result != NVML_SUCCESS) {
		UE_LOG(LogTemp, Error, TEXT("Failed to get clock rate: %s"), *FString(nvmlErrorString(result)));
		return 0.0f;
	}

	// 将时钟频率转换为浮点数并返回
	float clockFrequencyMHz = static_cast<float>(clock);
	return clockFrequencyMHz;
}

void UGPUFrequencyLibrary::TestGPU()
{
}



#if STATS

float UGPUFrequencyLibrary::GetStatInfo(const FString& StatName)//TEXT("Stat_GPU_SubsurfaceScattering")要先打开“启用数据分组（enable stat group）
{
	if (FGameThreadStatsData* StatsData = FLatestGameThreadStatsData::Get().Latest)
	{
		for (FActiveStatGroupInfo ActiveStatGroup : StatsData->ActiveStatGroups)
		{
			
				for (FComplexStatMessage CountersAggregate : ActiveStatGroup.CountersAggregate)
			{
				const double IncAveValueDouble = CountersAggregate.GetValue_double(EComplexStatField::IncAve);
				const double IncMaxValueDouble = CountersAggregate.GetValue_double(EComplexStatField::IncMax);
				const double IncMinValueDouble = CountersAggregate.GetValue_double(EComplexStatField::IncMin);
				// const double ExcAveValueDouble = CountersAggregate.GetValue_double(EComplexStatField::ExcAve);
				// const double ExcMaxValueDouble = CountersAggregate.GetValue_double(EComplexStatField::ExcMax);
				// const double ExcMinValueDouble = CountersAggregate.GetValue_double(EComplexStatField::ExcMin);
				FName Name = CountersAggregate.GetShortName();
				// UE_LOG(LogTemp, Warning, TEXT("%s"),*Name.ToString());
				// 使用UE_LOG打印这些值
				if(Name==*StatName)
				{
					UE_LOG(LogTemp, Warning, TEXT("Name: %s, IncAveValueDouble: %f, IncMaxValueDouble: %f, IncMinValueDouble: %f"), *Name.ToString(), IncAveValueDouble, IncMaxValueDouble, IncMinValueDouble);
					return IncAveValueDouble;
				}
			}
		}
	}
	return 0.f; // 如果未找到匹配的统计消息，返回默认值
}

#endif

int32 UGPUFrequencyLibrary::GetTriangleCount(UStaticMesh* StaticMesh)
{
	if (!StaticMesh)
	{
		UE_LOG(LogTemp, Warning, TEXT("StaticMesh is nullptr!"));
		return 0;
	}

	int32 TotalTriangleCount = 0;
	for (int32 LODIndex = 0; LODIndex < StaticMesh->GetRenderData()->LODResources.Num(); ++LODIndex)
	{
		FStaticMeshLODResources& LODModel = StaticMesh->GetRenderData()->LODResources[LODIndex];
		// StaticMesh.lod
		TotalTriangleCount += LODModel.GetNumTriangles();
	}

	return TotalTriangleCount;
}
void ExecuteWindowsCommand(const FString& Command)
{
	FString OutStdOut, OutStdErr;
	int32 ReturnCode = -1;

	// 调用FPlatformProcess::ExecProcess执行命令
	FPlatformProcess::ExecProcess(*Command, nullptr, nullptr, nullptr, nullptr);

    
    
	// 输出命令执行结果
	UE_LOG(LogTemp, Warning, TEXT("Command Output: %s"), *OutStdOut);
	UE_LOG(LogTemp, Warning, TEXT("Command Error: %s"), *OutStdErr);
	UE_LOG(LogTemp, Warning, TEXT("Command Return Code: %d"), ReturnCode);
}
int32 UGPUFrequencyLibrary::SetGPUFrequency(int32 ClockFrequency)
{
	FString Command = FString::Printf(TEXT("nvidia-smi -lgc %d"), ClockFrequency);
	// 执行命令
	int32 ExitCode = system(TCHAR_TO_ANSI(*Command));
	return ExitCode;
}