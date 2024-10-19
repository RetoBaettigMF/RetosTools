#!/bin/bash

# Setze den Projektordner auf das aktuelle Verzeichnis
PROJECT_PATH=$(pwd)

if [ -d "venv" ]; then
    echo "Projekt scheint schon installiert zu sein."
    echo "Bitte lösche das Verzeichnis $PROJECT_PATH/venv und versuche es erneut."
    read -p "Drücke eine beliebige Taste zum Beenden..." -n1 -s
    exit 1
fi

# Erstelle das Virtual Environment
echo "Erstelle das Virtual Environment..."
python3 -m venv venv

# Aktiviere das Virtual Environment
echo "Aktiviere das Virtual Environment..."
source venv/bin/activate

# Installiere die Anforderungen
echo "Installiere die Anforderungen..."
pip install -r requirements.txt

# Deaktiviere das Virtual Environment
echo "Deaktiviere das Virtual Environment..."
deactivate

echo "Installation abgeschlossen."
read -p "Drücke eine beliebige Taste zum Beenden..." -n1 -s

