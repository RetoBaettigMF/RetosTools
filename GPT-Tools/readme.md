# GPT-Tools

Dieses Programm ist ein Demonstrator für GPT Funktionalität

Das Programm greift direkt auf das API von OpenAI bzw. Azure OpenAI zu.

## Installation

1. Stelle sicher, dass Python auf deinem Computer installiert ist.
2. Lade das Programm herunter und speichere es in einem Verzeichnis deiner Wahl.
3. Öffne die Kommandozeile oder das Terminal.
4. Navigiere zum Verzeichnis, in dem du das Programm gespeichert hast.
5. Installiere alle Abhängigkeiten und das venv mit dem Befehl `install.bat`
7. Setze den API Key (siehe nächstes Kapitel)

## Konfiguration

Alle Parameter der Applikation können inder Datei `settings.py` eingestellt werden.

## Verwendung

## API Key

Für das Programm ist ein API Key von OpenAI nötig.

Die Umgebungsvariable kann folgendermassen gesetzt werden vor dem Aufruf des Programmes:

`set OPENAI_API_KEY=sk-OAry...`

Für Azure AI muss ein Key von Azure AI gesetzt werden:

`set AZURE_OPENAI_KEY=88..`


## Lizenz

Copyright (c) 2024 Reto Bättig (reto@baettig.org)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.