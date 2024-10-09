// Fill out your copyright notice in the Description page of Project Settings.

using UnrealBuildTool;
using System.IO;
public class MetaHuman : ModuleRules
{
	private string ModulePath
	{
		get
		{
			return ModuleDirectory;
		}
	}	
	private string ThirdPartyPath
	{
		get
		{
			return Path.GetFullPath(Path.Combine(ModulePath,"ThirdParty"));
		}
	}
	public MetaHuman(ReadOnlyTargetRules Target) : base(Target)
	{
		// PrivateDependencyModuleNames.AddRange(new string[] { "NVAPI" });
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "HeadMountedDisplay" ,"RHI"});
		// 添加对 dxgi.lib 的依赖项
		// PublicAdditionalLibraries.Add("dxgi.lib");
		PublicIncludePaths.Add(Path.Combine(ThirdPartyPath,"includes"));
		// PublicIncludePaths.Add(Path.Combine(ThirdPartyPath,"includes/torch/csrc/api/include"));
		PublicAdditionalLibraries.Add(Path.Combine(ThirdPartyPath,"libs","nvml.lib"));
		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });
		
		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
