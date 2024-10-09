// Fill out your copyright notice in the Description page of Project Settings.


#include "SSSScreenSize.h"

#include <vector>
#include <tuple>
#include <algorithm>


#include "DrawDebugHelpers.h"
#include "Kismet/GameplayStatics.h"

// Sets default values
ASSSScreenSize::ASSSScreenSize()
{
	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
}

// Called when the game starts or when spawned
void ASSSScreenSize::BeginPlay()
{
	Super::BeginPlay();
	// 获取场景中所有带标签 'SSS' 的 Actor

	UGameplayStatics::GetAllActorsWithTag(GetWorld(), FName(TEXT("SSS")), FoundActors);
}

// Called every frame
void ASSSScreenSize::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	// 清空 rectangles 数组
	rectangles.Empty();
	FVector2D ScreenSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
	for (AActor* Actor : FoundActors)
	{
		// 获取 Actor 的本地包围框
		// FBox ActorBounds = Actor->GetComponentsBoundingBox();
		FBox ActorBounds = Actor->CalculateComponentsBoundingBoxInLocalSpace();
		FVector origin,extent;
		Actor->GetActorBounds(false,origin,extent,false);
		FVector A1,A2,B1,B2;
		bool isA1,isA2,isB1,isB2;
		A1=origin+extent;
		A2=origin-extent;
		// // 将旋转角度设置为90度
		// FRotator Rotation(0.f, 90.f, 0.f);
		//
		// // 将旋转转换为四元数
		// FQuat QuatRotation = FQuat(Rotation);
		//
		// // 使用四元数将向量绕 Z 轴旋转
		// FVector RotatedVector = QuatRotation.RotateVector(extent);
		FVector RotatedVector(-extent.X, extent.Y, extent.Z);
		FVector RotatedVector2(extent.X, -extent.Y, extent.Z);
		FVector RotatedVector3(extent.X, extent.Y, -extent.Z);
		
		B1=origin+RotatedVector;
		B2=origin-RotatedVector;
		FVector C1,C2,D1,D2;
		bool isC1,isC2,isD1,isD2;
		C1=origin+RotatedVector2;
		C2=origin-RotatedVector2;
		D1=origin+RotatedVector3;
		D2=origin-RotatedVector3;
// 		DrawDebugLine(
// 	 GetWorld(),  // 传入世界指针
// 	 A1,       // 线的起点
// 	 A2,         // 线的终点
// 	 FColor::Red,       // 线的颜色
// 	 false,       // 是否在屏幕上持续显示
// 	 100,    // 持续时间
// 	 0,           // 线的深度优先级
// 	 2.f          // 线的厚度
//  );
// 		DrawDebugLine(
// GetWorld(),  // 传入世界指针
// B1,       // 线的起点
// B2,         // 线的终点
// FColor::Blue,       // 线的颜色
// false,       // 是否在屏幕上持续显示
// 100,    // 持续时间
// 0,           // 线的深度优先级
// 2.f          // 线的厚度
// );
// 		DrawDebugLine(
//  GetWorld(),  // 传入世界指针
//  D1,       // 线的起点
//  D2,         // 线的终点
//  FColor::Red,       // 线的颜色
//  false,       // 是否在屏幕上持续显示
//  100,    // 持续时间
//  0,           // 线的深度优先级
//  2.f          // 线的厚度
// );
// 		DrawDebugLine(
// GetWorld(),  // 传入世界指针
// C1,       // 线的起点
// C2,         // 线的终点
// FColor::Blue,       // 线的颜色
// false,       // 是否在屏幕上持续显示
// 100,    // 持续时间
// 0,           // 线的深度优先级
// 2.f          // 线的厚度
// );
		// 获取 Actor 的位置
		FVector ActorLocation = Actor->GetActorLocation();
		// 检查包围框是否有效
		if (ActorBounds.IsValid)
		{
			// 获取包围框的最小和最大顶点
			FVector MinPoint = ActorBounds.Min;
			FVector MaxPoint = ActorBounds.Max;
			// 将包围框的顶点转换为屏幕空间坐标
			FVector2D ScreenMinPoint;
			FVector2D ScreenMaxPoint;
			FVector2D ScreenA1,ScreenA2,ScreenB1,ScreenB2;
			FVector2D ScreenC1,ScreenC2,ScreenD1,ScreenD2;
			UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
				ActorLocation +
				MinPoint, ScreenMinPoint);
			UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
				ActorLocation +
				MaxPoint, ScreenMaxPoint);
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
				A1, ScreenA1))
			{
				isA1=true;
			}else
			{
				isA1=false;
			}
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
				A2, ScreenA2))
			{
				isA2=true;
			}else
			{
				isA2=false;
			}
			;
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
			B1, ScreenB1)){
				isB1=true;
			}else
			{
				isB1=false;
			}
			;
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
			B2, ScreenB2)){
				isB2=true;
			}else
			{
				isB2=false;
			}
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
			C1, ScreenC1)){
				isC1=true;
			}else
			{
				isC1=false;
			}
			;
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
			C2, ScreenC2)){
				isC2=true;
			}else
			{
				isC2=false;
			}
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
			D1, ScreenD1)){
				isD1=true;
			}else
			{
				isD1=false;
			}
			;
			if(UGameplayStatics::GetPlayerController(GetWorld(), 0)->ProjectWorldLocationToScreen(
			D2, ScreenD2)){
				isD2=true;
			}else
			{
				isD2=false;
			}
			;
			// 获取屏幕边界,交换为最小到最大
			exchangedMinMax(ScreenA1,ScreenA2);
			exchangedMinMax(ScreenB1,ScreenB2);
			exchangedMinMax(ScreenC1,ScreenC2);
			exchangedMinMax(ScreenD1,ScreenD2);
			UE_LOG(LogTemp, Warning, TEXT("ScreenA1: %s"), *ScreenA1.ToString());
			UE_LOG(LogTemp, Warning, TEXT("ScreenA2: %s"), *ScreenA2.ToString());
			UE_LOG(LogTemp, Warning, TEXT("ScreenB1: %s"), *ScreenB1.ToString());
			UE_LOG(LogTemp, Warning, TEXT("ScreenB2: %s"), *ScreenB2.ToString());

			UE_LOG(LogTemp, Warning, TEXT("ScreenC1: %s"), *ScreenC1.ToString());
			UE_LOG(LogTemp, Warning, TEXT("ScreenC2: %s"), *ScreenC2.ToString());
			UE_LOG(LogTemp, Warning, TEXT("ScreenD1: %s"), *ScreenD1.ToString());
			UE_LOG(LogTemp, Warning, TEXT("ScreenD2: %s"), *ScreenD2.ToString());

			ScreenA1.X = FMath::Clamp(ScreenA1.X, 0.f, ScreenSize.X);
			ScreenA1.Y = FMath::Clamp(ScreenA1.Y, 0.f, ScreenSize.Y);
			ScreenA2.X = FMath::Clamp(ScreenA2.X, 0.f, ScreenSize.X);
			ScreenA2.Y = FMath::Clamp(ScreenA2.Y, 0.f, ScreenSize.Y);
			
			ScreenB1.X = FMath::Clamp(ScreenB1.X, 0.f, ScreenSize.X);
			ScreenB1.Y = FMath::Clamp(ScreenB1.Y, 0.f, ScreenSize.Y);
			ScreenB2.X = FMath::Clamp(ScreenB2.X, 0.f, ScreenSize.X);
			ScreenB2.Y = FMath::Clamp(ScreenB2.Y, 0.f, ScreenSize.Y);

			ScreenC1.X = FMath::Clamp(ScreenC1.X, 0.f, ScreenSize.X);
			ScreenC1.Y = FMath::Clamp(ScreenC1.Y, 0.f, ScreenSize.Y);
			ScreenC2.X = FMath::Clamp(ScreenC2.X, 0.f, ScreenSize.X);
			ScreenC2.Y = FMath::Clamp(ScreenC2.Y, 0.f, ScreenSize.Y);

			ScreenD1.X = FMath::Clamp(ScreenD1.X, 0.f, ScreenSize.X);
			ScreenD1.Y = FMath::Clamp(ScreenD1.Y, 0.f, ScreenSize.Y);
			ScreenD2.X = FMath::Clamp(ScreenD2.X, 0.f, ScreenSize.X);
			ScreenD2.Y = FMath::Clamp(ScreenD2.Y, 0.f, ScreenSize.Y);
			if(isA1&&isA2)
			{
				rectangles.Add(FIntRect(FMath::RoundToInt(ScreenA1.X), FMath::RoundToInt(ScreenA1.Y),
									FMath::RoundToInt(ScreenA2.X), FMath::RoundToInt(ScreenA2.Y)));
			}else
			{
				UE_LOG(LogTemp, Warning, TEXT("%s %s %d ==> A error"), *FString(__FUNCTION__), *FString(__FILE__),
				       __LINE__);
			}
			if(isB1&&isB2)
			{
				rectangles.Add(FIntRect(FMath::RoundToInt(ScreenB1.X), FMath::RoundToInt(ScreenB1.Y),
									FMath::RoundToInt(ScreenB2.X), FMath::RoundToInt(ScreenB2.Y)));
			}else
			{
				UE_LOG(LogTemp, Warning, TEXT("%s %s %d ==> B error"), *FString(__FUNCTION__), *FString(__FILE__),
					   __LINE__);
			}
			if(isC1&&isC2)
			{
				rectangles.Add(FIntRect(FMath::RoundToInt(ScreenC1.X), FMath::RoundToInt(ScreenC1.Y),
									FMath::RoundToInt(ScreenC2.X), FMath::RoundToInt(ScreenC2.Y)));
			}else
			{
				UE_LOG(LogTemp, Warning, TEXT("%s %s %d ==> C error"), *FString(__FUNCTION__), *FString(__FILE__),
					   __LINE__);
			}
			if(isD1&&isD2)
			{
				rectangles.Add(FIntRect(FMath::RoundToInt(ScreenD1.X), FMath::RoundToInt(ScreenD1.Y),
									FMath::RoundToInt(ScreenD2.X), FMath::RoundToInt(ScreenD2.Y)));
			}else
			{
				UE_LOG(LogTemp, Warning, TEXT("%s %s %d ==> D error"), *FString(__FUNCTION__), *FString(__FILE__),
					   __LINE__);
			}
			
			
			// // 打印矩形A
			// UE_LOG(LogTemp, Warning, TEXT("Rectangle A: (%d, %d, %d, %d)"), 
			// 	FMath::RoundToInt(ScreenA1.X), FMath::RoundToInt(ScreenA1.Y),
			// 	FMath::RoundToInt(ScreenA2.X), FMath::RoundToInt(ScreenA2.Y));
			//
			// // 打印矩形B
			// UE_LOG(LogTemp, Warning, TEXT("Rectangle B: (%d, %d, %d, %d)"), 
			// 	FMath::RoundToInt(ScreenB1.X), FMath::RoundToInt(ScreenB1.Y),
			// 	FMath::RoundToInt(ScreenB2.X), FMath::RoundToInt(ScreenB2.Y));
			// int tempMin,tempMax;
			// tempMin=FMath::Min(ScreenMinPoint.X, ScreenMaxPoint.X);
			// tempMax=FMath::Max(ScreenMinPoint.X, ScreenMaxPoint.X);
			// ScreenMinPoint.X=tempMin;
			// ScreenMaxPoint.X=tempMax;
			// tempMin=FMath::Min(ScreenMinPoint.Y, ScreenMaxPoint.Y);
			// tempMax=FMath::Max(ScreenMinPoint.Y, ScreenMaxPoint.Y);
			// ScreenMinPoint.Y=tempMin;
			// ScreenMaxPoint.Y=tempMax;
			//
			// // 确保屏幕空间坐标在有效范围内
			// ScreenMinPoint.X = FMath::Clamp(ScreenMinPoint.X, 0.f, ScreenSize.X);
			// ScreenMinPoint.Y = FMath::Clamp(ScreenMinPoint.Y, 0.f, ScreenSize.Y);
			// ScreenMaxPoint.X = FMath::Clamp(ScreenMaxPoint.X, 0.f, ScreenSize.X);
			// ScreenMaxPoint.Y = FMath::Clamp(ScreenMaxPoint.Y, 0.f, ScreenSize.Y);
			// // 将屏幕空间坐标保存到 TArray<TArray<INT32>> rectangles; 结构中
			// rectangles.Add(FIntRect(FMath::RoundToInt(ScreenMinPoint.X), FMath::RoundToInt(ScreenMinPoint.Y),
			// 						FMath::RoundToInt(ScreenMaxPoint.X), FMath::RoundToInt(ScreenMaxPoint.Y)));
			// 输出最小和最大顶点的信息
			// UE_LOG(LogTemp, Warning, TEXT("Actor %s Min Point: %s"), *Actor->GetName(), *MinPoint.ToString());
			// UE_LOG(LogTemp, Warning, TEXT("Actor %s Max Point: %s"), *Actor->GetName(), *MaxPoint.ToString());
		}
		else
		{
			// 如果包围框无效，则输出警告信息
			UE_LOG(LogTemp, Warning, TEXT("Actor has invalid bounding box!"));
		}
	}
	// for (const FIntRect& Rectangle : rectangles)
	// {
	// 	UE_LOG(LogTemp, Warning, TEXT("Rectangle: (%d, %d, %d, %d)"), Rectangle.Min.X, Rectangle.Min.Y, Rectangle.Max.X,
	// 	       Rectangle.Max.Y);
	// }

	// 计算矩形面积
	if(rectangles.Num()>0)
	{
		int area = rectangleArea();
		UE_LOG(LogTemp, Warning, TEXT("Total area: %d"), area);
		UE_LOG(LogTemp, Warning, TEXT("Total screen area %d* %d: %d"), static_cast<int>(ScreenSize.X ),static_cast<int>( ScreenSize.Y),static_cast<int>(ScreenSize.X * ScreenSize.Y));
		UE_LOG(LogTemp, Warning, TEXT("屏幕占比: %d"), static_cast<int>(100.0*area/(ScreenSize.X * ScreenSize.Y)));
		FinalScreenSize=static_cast<int>(100.0*area/(ScreenSize.X * ScreenSize.Y));
	}else
	{
		UE_LOG(LogTemp, Warning, TEXT("屏幕占比: 0"));
		FinalScreenSize=0;
	}
	
}

// 矩形面积计算函数
int ASSSScreenSize::rectangleArea()
{
	int n = rectangles.Num();
	std::vector<int> hbound;
	for (const auto& rect : rectangles)
	{
		// 下边界
		hbound.push_back(rect.Min.Y);
		// 上边界
		hbound.push_back(rect.Max.Y);
	}
	std::sort(hbound.begin(), hbound.end());
	hbound.erase(unique(hbound.begin(), hbound.end()), hbound.end());
	int m = hbound.size();
	// length[i] 可以通过 hbound[i+1] - hbound[i] 得到
	std::vector<int> seg(m - 1);

	std::vector<std::tuple<int, int, int>> sweep;
	for (int i = 0; i < n; ++i)
	{
		// 左边界
		sweep.emplace_back(rectangles[i].Min.X, i, 1);
		// 右边界
		sweep.emplace_back(rectangles[i].Max.X, i, -1);
	}
	std::sort(sweep.begin(), sweep.end());

	


	
	long long ans = 0;
	for (int i = 0; i < sweep.size(); ++i)
	{
		int j = i;
		while (j + 1 < sweep.size() && std::get<0>(sweep[i]) == std::get<0>(sweep[j + 1]))
		{
			++j;
		}
		if (j + 1 == sweep.size())
		{
			break;
		}
		// 一次性地处理掉一批横坐标相同的左右边界
		for (int k = i; k <= j; ++k)
		{
			// auto&& [_, idx, diff] = sweep[k];
			int _;
			int idx;
			int diff;
			std::tie(_, idx, diff) = sweep[k];
			int left = rectangles[idx].Min.Y, right = rectangles[idx].Max.Y;
			for (int x = 0; x < m - 1; ++x)
			{
				if (left <= hbound[x] && hbound[x + 1] <= right)
				{
					seg[x] += diff;
				}
			}
		}
		int cover = 0;
		for (int k = 0; k < m - 1; ++k)
		{
			if (seg[k] > 0)
			{
				cover += (hbound[k + 1] - hbound[k]);
			}
		}
		ans += static_cast<long long>(cover) * (std::get<0>(sweep[j + 1]) - std::get<0>(sweep[j]));
		i = j;
	}
	return ans;
}
void ASSSScreenSize::exchangedMinMax(FVector2D& Min, FVector2D& Max)
{
	int tempMin,tempMax;
	tempMin=FMath::Min(Min.X, Max.X);
	tempMax=FMath::Max(Min.X, Max.X);
	Min.X=tempMin;
	Max.X=tempMax;
	tempMin=FMath::Min(Min.Y, Max.Y);
	tempMax=FMath::Max(Min.Y, Max.Y);
	Min.Y=tempMin;
	Max.Y=tempMax;
}
//
// // 线段树初始化函数
// void ASSSScreenSize::init(int idx, int l, int r)
// {
// 	tree[idx].cover = tree[idx].length = 0;
// 	if (l == r)
// 	{
// 		tree[idx].max_length = hbound[l] - hbound[l - 1];
// 		return;
// 	}
// 	int mid = (l + r) / 2;
// 	init(idx * 2, l, mid);
// 	init(idx * 2 + 1, mid + 1, r);
// 	tree[idx].max_length = tree[idx * 2].max_length + tree[idx * 2 + 1].max_length;
// }
//
// // 更新线段树节点信息
// void ASSSScreenSize::update(int idx, int l, int r, int ul, int ur, int diff)
// {
// 	if (l > ur || r < ul)
// 	{
// 		return;
// 	}
// 	if (ul <= l && r <= ur)
// 	{
// 		tree[idx].cover += diff;
// 		pushup(idx, l, r);
// 		return;
// 	}
// 	int mid = (l + r) / 2;
// 	update(idx * 2, l, mid, ul, ur, diff);
// 	update(idx * 2 + 1, mid + 1, r, ul, ur, diff);
// 	pushup(idx, l, r);
// }
//
// // 更新线段树节点信息
// void ASSSScreenSize::pushup(int idx, int l, int r)
// {
// 	if (tree[idx].cover > 0)
// 	{
// 		tree[idx].length = tree[idx].max_length;
// 	}
// 	else if (l == r)
// 	{
// 		tree[idx].length = 0;
// 	}
// 	else
// 	{
// 		tree[idx].length = tree[idx * 2].length + tree[idx * 2 + 1].length;
// 	}
// }

int ASSSScreenSize::GetSSSLOD(){return FinalScreenSize;}