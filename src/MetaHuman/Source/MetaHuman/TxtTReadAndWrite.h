// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "TxtTReadAndWrite.generated.h"

/**
 * 
 */
UCLASS()
class METAHUMAN_API UTxtTReadAndWrite : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:

	UFUNCTION(BlueprintCallable, Category = "MyLibrary")
	static FString ReadTxt(FString path);

	UFUNCTION(BlueprintCallable, Category = "MyLibrary")
	static bool WriteTxt(FString saveString, FString path);
};

