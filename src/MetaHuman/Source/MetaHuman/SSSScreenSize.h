// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SSSScreenSize.generated.h"

// 结构体用于表示线段树的节点
struct Segtree {
	int cover;
	int length;
	int max_length;
};

UCLASS()
class METAHUMAN_API ASSSScreenSize : public AActor
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	ASSSScreenSize();

	// Called every frame
	virtual void Tick(float DeltaTime) override;
	
	int FinalScreenSize;
	
	UFUNCTION(BlueprintCallable)
	int GetSSSLOD();
protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

private:
	// 声明线段树成员变量
	TArray<Segtree> tree;
	// TArray<int> hbound;

	// 其他成员函数声明
	int rectangleArea();
	void exchangedMinMax(FVector2D& Min, FVector2D& Max);
	// 其他成员变量声明
	TArray<FIntRect> rectangles;
	TArray<AActor*> FoundActors;
};