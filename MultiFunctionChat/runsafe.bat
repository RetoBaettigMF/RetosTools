@echo off

REM Setze den Projektordner auf das aktuelle Verzeichnis
cd run
set PROJECT_PATH=%cd%
echo Project Path = %PROJECT_PATH%

if exist "venv" (
    echo Projekt scheint schon installiert zu sein.
    goto :continue 
)

REM Erstelle das Virtual Environment
echo Erstelle das Virtual Environment...
python -m venv venv

REM Aktiviere das Virtual Environment
echo Aktiviere das Virtual Environment...
call venv\Scripts\activate.bat

:continue
call run.bat
call venv\Scripts\deactivate.bat
