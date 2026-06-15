; MeshCADCreate Windows Installer with Icon + Wizard
#define MyAppName "MeshCADCreate"
#define MyAppVersion "1.0"
#define MyAppPublisher "Perth Resoles"
#define MyAppExeName "meshcad.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
WizardStyle=modern
SetupIconFile=meshcad_icon.ico
WizardImageFile=wizard_image.bmp

[Files]
Source: "dist\meshcad.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"
Source: "LICENSE"; DestDir: "{app}"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
