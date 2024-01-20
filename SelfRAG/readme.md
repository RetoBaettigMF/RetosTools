# SelfRAG

Dieses Programm ist ein Demonstrator für RAG (Retrieval Augmented Generation), welches den folgenden Prozess durchführt
1. (falls `vectordb.json` gefunden wird wird direkt bei Punkt 5 weitergefahren)
2. Aufteilen der Daten in "verdaubare" chunks
3. Berechnung der Embedding Vektoren für die chunks
4. Speichern der Vektoren in `vectordb.json`
5. Finden der nächsten Vektoren für einen bestimmten Prompt
6. Erstellen eines RAG-Prompts und erstellen einer Antwort aufgrund der eingelernten Daten

Das Programm greift direkt auf das API von OpenAI zu.

## Installation

1. Stelle sicher, dass Python auf deinem Computer installiert ist.
2. Lade das Programm herunter und speichere es in einem Verzeichnis deiner Wahl.
3. Öffne die Kommandozeile oder das Terminal.
4. Navigiere zum Verzeichnis, in dem du das Programm gespeichert hast.
5. Installiere alle Abhängigkeiten und das venv mit dem Befehl `install.bat`
6. Kopiere die zu trainierenden Datein in das verzeichnis `\data`
7. Setze den API Key (siehe nächstes Kapitel)


## Verwendung
1. Aktiviere das virtuelle Environment mit `activate_venv.bat`
2. Führe das Programm mit dem Befehl `python main.py` 


## API Key

Für das Programm ist ein API Key von OpenAI nötig.

Die Umgebungsvariable kann folgendermassen gesetzt werden vor dem Aufruf des Programmes:

`set OPENAI_API_KEY=sk-OAry...`

## Lizenz

Copyright (c) 2024 Reto Bättig (reto@baettig.org)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.