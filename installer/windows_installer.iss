; MeshCADCreate Windows Installer Script
#define MyAppName "MeshCADCreate"
#define MyAppVersion "1.0"
#define MyAppPublisher "Perth Resoles"
#define MyAppExeName "meshcad.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename=MeshCADCreate_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\meshcad.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
