; Para TudiViewer
; J.Abian 10 september 2012

#define MyAppName ReadIni(SourcePath + "install.ini", "Common", "name", "noname")
#define MyVersion ReadIni(SourcePath + "install.ini", "Common", "version", "0.0.0")
#define MyIconDir ReadIni(SourcePath + "install.ini", "Common", "icondir", "")
#define MyWizardDir ReadIni(SourcePath + "install.ini","Inno", "wzdir", "")
#define MyBigIcon ReadIni(SourcePath + "install.ini", "Common", "big_icon", "")
#define MySmallIcon ReadIni(SourcePath + "install.ini", "Inno","small_icon", "")
#define MyWizardImage ReadIni(SourcePath + "install.ini","Inno","wzimg","")
#define MyWizardSecondImage ReadIni(SourcePath + "install.ini","Inno","wzsimg","")
#define MyPswd ReadIni(SourcePath + "install.ini", "Inno", "pswd", "lpcsicuab")
#define MyComment "Blast peptide collections and analyzes results"
#define MyInstall "INSTALL.txt"

[Setup]
AppName={#MyAppName}
;data for unins000.dat file
AppId={#MyAppName} {#MyVersion}
;appears in the first page of the installer
;AppVerName={cm:NameAndVersion,KimBlast,{cm:Myvers}}
;appears in the support info for add/remove programs
AppVersion={#MyVersion}
AppPublisher=Joaquin Abian
DefaultDirName={pf}\{#MyAppName}_{#MyVersion}
UsePreviousAppDir=no
DefaultGroupName=KimKaos
Compression=lzma/max
AllowNoIcons=yes
AllowRootDirectory=yes
UsePreviousLanguage=no
UninstallDisplayIcon={#MyIconDir}\{#MySmallIcon}
OutputBaseFilename={#MyAppName}_{#MyVersion}_setup
OutputDir=installer
InfoAfterFile={#MyInstall}
LicenseFile="LICENCE.txt"
Password={#MyPswd}
WizardImageFile={#MyWizardDir}\{#MyWizardImage}
#ifdef MyWizardSecondImage
  WizardSmallImageFile={#MyWizardDir}\{#MyWizardSecondImage}
#endif
AppCopyright=Pending 2010 Joaquin Abian
;appears in properties "version del archivo" and "version del producto"
;of the Setup.exe program in the "Version" page
;and also in the info when Setup.exe is selected with the cursor and where it adds a zero
VersionInfoVersion={#MyVersion}
SetupIconFile={#MyIconDir}\{#MyBigIcon}

[Files]
Source: "test\*"; DestDir: "{app}\test"
Source: "dist\*"; DestDir: "{app}"
Source :{#MyIconDir}\{#MySmallIcon}; DestDir:{app}
#if FileExists(SourcePath + "dist\mpl-data\matplotlibrc")
  Source: "dist\mpl-data\*"; DestDir: "{app}\mpl-data"
  Source: "dist\mpl-data\images\*"; DestDir: "{app}\mpl-data\images"
#endif

#if FileExists(SourcePath + "dist\doc\README.html")
  Source: "dist\doc\*"; DestDir: "{app}\doc"
#endif

[Tasks]
;CreateDesktopIcon is defined in Default.isl
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"

[Icons]
Name: "{group}\{#MyAppName} {#MyVersion}"; Filename: "{app}\{#MyAppName}.exe" ; IconFilename:{app}\{#MySmallIcon};WorkingDir: "{app}"; Comment: {#MyComment}
Name: "{userdesktop}\{#MyAppName} {#MyVersion}"; Filename: "{app}\{#MyAppName}.exe"; WorkingDir: "{app}"; Tasks: desktopicon


