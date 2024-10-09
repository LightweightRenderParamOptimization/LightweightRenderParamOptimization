#pragma once

#define WIN32_LEAN_AND_MEAN
// #include "Windows.h"

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "nvml.h"
// #include <dxgi1_4.h>
// #include "Windows/AllowWindowsPlatformTypes.h"
// #include "Windows/HideWindowsPlatformTypes.h"

// 如果需要包含 nvapi 头文件，将其放在其他库之前
// #include "nvapi_lite_common.h"
// #include "nvapi.h"

#include "GPUFrequencyLibrary.generated.h"


/**
 * 
 */
UCLASS()
class METAHUMAN_API UGPUFrequencyLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:
	
	~UGPUFrequencyLibrary();
	UFUNCTION(BlueprintCallable, Category = "MyLibrary")
	static void  TestGPU();

	UFUNCTION(BlueprintCallable, Category = "MyLibrary")
	static float GetGPUClockFrequency();
	/**
	 * Get statistical information for a given statistic.
	 *
	 * @param StatName The name of the statistic to query.
	 * @return The average time for the specified statistic.
	 */
	UFUNCTION(BlueprintCallable, Category = "MyStatsLibrary")
	static float GetStatInfo(const FString& StatName);
	struct FrequencyInfo
	{
		unsigned int NvGraphicsClockInMhz;
	};
	UFUNCTION(BlueprintCallable, Category = "MyStatsLibrary")
	static int32 GetTriangleCount(UStaticMesh* StaticMesh);
	


	UFUNCTION(BlueprintCallable, Category = "MyStatsLibrary")
	static int32 SetGPUFrequency(int32 ClockFrequency);

public:
	

	UGPUFrequencyLibrary();
	

	// bool static Init();
	

	// bool static GetCoreClockMhz(FrequencyInfo *pInfo);
	
private:
	// NvPhysicalGpuHandle static m_GpuHandle;
};
