// Fill out your copyright notice in the Description page of Project Settings.


#include "GPUTimeInfo.h"

#include "GPUProfiler.h"
#include "Renderer/Private/SceneRendering.h"

/** How many cycles the renderthread used (excluding idle time). It's set once per frame in FViewport::Draw. */
extern RENDERCORE_API uint32 GRenderThreadTime;
/** How many cycles the gamethread used (excluding idle time). It's set once per frame in FViewport::Draw. */
extern RENDERCORE_API uint32 GGameThreadTime;
/** How many cycles it took to swap buffers to present the frame. */
extern RENDERCORE_API uint32 GSwapBufferTime;

float METAHUMAN_API UGPUTimeInfo::GetSubsurfaceScatteringAvgTime()
{
	// // 获取 GPU 性能分析器
	// FGPUProfiler& GPUProfiler = FSceneRenderer::GetGPUProfiler();
	// // 获取当前 GPU 事件树
	// TArray<TRefCountPtr<FGPUProfilerEventNode>> EventTree;
	// GatherStatsEventNode()
	// TArray< TRefCountPtr< FGPUProfilerEventNode > > EventTree=FGPUProfiler::CurrentEventNodeFrame->EventTree;
	// // 检查是否有 SubsurfaceScattering 数据
	// if (GPUProfiler.HasFrameData(FGPUProfiler::EKey::SubsurfaceScattering))
	// {
	// 	// 获取 SubsurfaceScattering 数据
	// 	const TArray<float>& SubsurfaceScatteringData = GPUProfiler.GetFrameData<float>(FGPUProfiler::EKey::SubsurfaceScattering);
	//
	// 	// 输出当前帧 SubsurfaceScattering 值
	// 	for (float Value : SubsurfaceScatteringData)
	// 	{
	// 		UE_LOG(LogTemp, Warning, TEXT("SubsurfaceScattering: %f"), Value);
	// 	}
	// }
	// else
	// {
	// 	// 没有 SubsurfaceScattering 数据
	// 	UE_LOG(LogTemp, Warning, TEXT("No SubsurfaceScattering data available for this frame."));
	// }




	 float CurrentTime = FApp::GetCurrentTime();
	 float DeltaTime = CurrentTime - FApp::GetLastTime();

	// Number of milliseconds in total last frame
	float RawFrameTime = DeltaTime * 1000.0;

	// // Number of milliseconds the gamethread was used last frame
	//  float RawGameThreadTime = FPlatformTime::ToMilliseconds(GGameThreadTime);
	//
	// // Number of milliseconds the renderthread was used last frame
	//  float RawRenderThreadTime = FPlatformTime::ToMilliseconds(GRenderThreadTime);

	// Number of milliseconds the GPU was busy last frame
	uint32 GPUCycles = RHIGetGPUFrameCycles();
	float RawGPUFrameTime = FPlatformTime::ToMilliseconds(GPUCycles);
	return RawGPUFrameTime;
}
