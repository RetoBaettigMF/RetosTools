@echo off

REM Setze den Projektordner auf das aktuelle Verzeichnis
cd run
set PROJECT_PATH=%cd%
echo Project Path = %PROJECT_PATH%

if exist "venv" (
    goto :continue 
)

REM Erstelle das Virtual Environment
echo Erstelle das Virtual Environment...
python -m venv venv

:continue

IF NOT EXIST "run.bat" (
    echo Error: The file 'run.bat' does not exist.
    goto :end
)
REM Aktiviere das Virtual Environment
echo Aktiviere das Virtual Environment...
call venv\Scripts\activate.bat
call run.bat
call venv\Scripts\deactivate.bat

:end