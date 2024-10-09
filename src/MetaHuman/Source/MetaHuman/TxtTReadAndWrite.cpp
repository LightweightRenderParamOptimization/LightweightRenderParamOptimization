// Fill out your copyright notice in the Description page of Project Settings.


#include "TxtTReadAndWrite.h"

FString UTxtTReadAndWrite::ReadTxt(FString path)
{
	FString resultString;

	FFileHelper::LoadFileToString(resultString, *(FPaths::ProjectContentDir() + path));

	return resultString;
}

bool UTxtTReadAndWrite::WriteTxt(FString saveString, FString path)
{
	bool result;
	
	result = FFileHelper::SaveStringToFile(saveString, *(FPaths::ProjectContentDir() + path));
	
	return result;
}
