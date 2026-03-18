[Setup]
AppId={{A1D5E4B2-9F8B-4D7B-9A0A-1C2D3E4F5A6B}}
AppName=NetBoot X
AppVersion=1.0.0
AppPublisher=Blue
AppPublisherURL=https://ln.ki/Blue.tcc
AppSupportURL=https://ln.ki/Blue.tcc
AppUpdatesURL=https://ln.ki/Blue.tcc
DefaultDirName={autopf}\NetBoot X
DefaultGroupName=NetBoot X
DisableProgramGroupPage=yes
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer_output
OutputBaseFilename=NetBootX_Setup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\NetBootX.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\NetBootX.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace

[Icons]
Name: "{group}\NetBoot X"; Filename: "{app}\NetBootX.exe"
Name: "{autodesktop}\NetBoot X"; Filename: "{app}\NetBootX.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NetBootX.exe"; Description: "Launch NetBoot X"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\NetBootX"

[Code]
// ฟังก์ชันปิด NetBootX.exe ถ้ามันเปิดอยู่
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // ปิด NetBootX.exe แบบ force
  Exec('taskkill', '/F /IM NetBootX.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := True;
end;