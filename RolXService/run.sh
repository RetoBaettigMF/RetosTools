#!/bin/bash

# Setze den Projektordner auf das aktuelle Verzeichnis
PROJECT_PATH=$(pwd)
PROJECT_PATH=/root/RetosTools/RolXService

echo "$PROJECT_PATH/venv"
cd $PROJECT_PATH

if [ -d "$PROJECT_PATH/venv" ]; then
    echo "Projekt ist installiert"
else
    echo "Projekt noch nicht installiert. Rufe zuerst install auf"
    read -p "Drücke eine beliebige Taste zum Beenden..." -n1 -s
    return 1
fi

# Aktiviere das Virtual Environment
echo "Aktiviere das Virtual Environment..."
source venv/bin/activate

source ~/setkeys.sh

python service.py

