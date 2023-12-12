# Web Scraper

Dieses Programm ist ein Web Scraper, der verwendet wird, um den Inhalt einer Webseite herunterzuladen und in Markdown-Dateien zu speichern. Es verwendet die Python-Bibliotheken `requests`, `BeautifulSoup`, `html2text` und `os`.

## Installation

1. Stelle sicher, dass Python auf deinem Computer installiert ist.
2. Lade das Programm herunter und speichere es in einem Verzeichnis deiner Wahl.

## Verwendung

1. Öffne die Kommandozeile oder das Terminal.
2. Navigiere zum Verzeichnis, in dem du das Programm gespeichert hast.
3. Installiere alle Abhängigkeiten mit dem Befehl `install.bat`
4. Führe das Programm mit dem Befehl `python scraper.py [URL]` aus, wobei `[URL]` die URL der Webseite ist, die du durchsuchen möchtest.

Das Programm durchsucht die Webseite und speichert den Inhalt in Markdown-Dateien im Verzeichnis `results/`. Die Dateien werden numerisch nummeriert und enthalten den Titel der Webseite als Überschrift.

Am Schluss wird eine Datei `result.md` erstellt, in welcher sämtliche Inhalte zusammengefügt sind.

## Hinweise

- Stelle sicher, dass du eine stabile Internetverbindung hast, um das Programm ordnungsgemäß auszuführen.
- Das Programm unterstützt nur Webseiten, die HTML als Antwort zurückgeben.
- Das Programm ignoriert Links, die mit "#" beginnen, E-Mail-Links und JavaScript-Links.

Viel Spaß beim Verwenden des Web Scrapers! Wenn du weitere Fragen hast, stehe ich gerne zur Verfügung.

## Lizenz

Copyright (c) 2023 Reto Bättig (reto@baettig.org)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.