@echo off

REM Setze den Projektordner auf das aktuelle Verzeichnis
set PROJECT_PATH=%cd%

if exist "venv" (
    echo Projekt scheint schon installiert zu sein.
    echo Bitte lösche das sonst das Verzeichnis %PROJECT_PATH%\venv und versuche es erneut.
    pause
    goto :exit 
)

REM Erstelle das Virtual Environment
echo Erstelle das Virtual Environment...
python -m venv venv

REM Aktiviere das Virtual Environment
echo Aktiviere das Virtual Environment...
call venv\Scripts\activate.bat

REM Installiere die Anforderungen
echo Installiere die Anforderungen...
pip install -r requirements.txt

REM Deaktiviere das Virtual Environment
echo Deaktiviere das Virtual Environment...
deactivate

:exit
echo Installation abgeschlossen.
pause