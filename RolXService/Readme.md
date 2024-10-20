
## Installation und start der Anwendung

**Installation**`

Die installation erstellt zuerst ein virtuelles environment uns installiert alle benötigten python pakete:
```
install.bat
```

**Starten die Anwendung:**

Setze zuerst die secrets in ..\setkey.bat

```bash
activate_venv
python service.py
```

**Teste den den Webservice:**

gehe mit einem Browser auf [localhost:5000/api/test](https://localhost:5000/api/)

```bash
python unittests.py
```

## Installation als Service auf ubuntu
```
cp rolxservice.service /etc/systemd/system/
systemctl daemon-reload
systemctl start rolxservice.service
```

Um sicherzustellen, dass der Dienst beim Booten automatisch gestartet wird, führe Folgendes aus:

```bash
systemctl enable rolxservice.service
```

**Dienststatus überprüfen**

Du kannst den Status deines Dienstes überprüfen mit:

```bash
sudo systemctl status rolxservice.service
```

**Logs überprüfen**

Um die Logs deines Dienstes zu sehen, kannst du `journalctl` verwenden:

```bash
journalctl -u rolxservice.service
```


## Selbsterstelltes Zertifikat

**Erstelle ein selbstsigniertes SSL-Zertifikat für Entwicklungszwecke:**

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

*Hinweis:* Dieses Zertifikat ist nicht für Produktionsumgebungen geeignet.

## Erstelle ein Let's Encrypt Zertifikat:
Um ein SSL-Zertifikat für deine Flask-Anwendung auf dem Server `baettig.org` zu erstellen, kannst du Let's Encrypt verwenden, das kostenlose SSL-Zertifikate anbietet. Hier sind die Schritte, um ein SSL-Zertifikat zu erstellen und es in deiner Flask-Anwendung zu verwenden:

### Schritt 1: Installiere Certbot

Certbot ist ein Tool, das dir hilft, SSL-Zertifikate von Let's Encrypt zu erhalten und zu verwalten. Installiere Certbot auf deinem Server:

Für Ubuntu/Debian:
```bash
sudo apt update
sudo apt install certbot
```

Für CentOS/RHEL:
```bash
sudo yum install certbot
```

### Schritt 2: Erhalte das SSL-Zertifikat

Führe den folgenden Befehl aus, um ein SSL-Zertifikat für deine Domain zu erhalten. Ersetze `baettig.org` durch deine tatsächliche Domain:

```bash
sudo certbot certonly --standalone -d baettig.org
```

Dieser Befehl startet den Certbot im Standalone-Modus, der einen temporären Webserver startet, um die Domain-Validierung durchzuführen. Stelle sicher, dass Port 80 (HTTP) und 443 (HTTPS) in deiner Firewall geöffnet sind.

### Schritt 3: Zertifikate finden

Nach erfolgreicher Ausführung findest du die Zertifikate in folgendem Verzeichnis:
- Zertifikat: `/etc/letsencrypt/live/baettig.org/fullchain.pem`
- Privater Schlüssel: `/etc/letsencrypt/live/baettig.org/privkey.pem`

### Schritt 4: Konfiguriere deine Flask-Anwendung

Ändere die `app.run()`-Zeile in deiner Flask-Anwendung, um die neuen Zertifikate zu verwenden:

```python
app.run(host='0.0.0.0', port=5000, ssl_context=('/etc/letsencrypt/live/baettig.org/fullchain.pem', '/etc/letsencrypt/live/baettig.org/privkey.pem'))
```

### Schritt 5: Automatisiere die Zertifikatserneuerung

Let's Encrypt-Zertifikate sind nur 90 Tage gültig. Du kannst die Erneuerung automatisieren, indem du einen Cron-Job hinzufügst. Führe den folgenden Befehl aus, um den Crontab-Editor zu öffnen:

```bash
sudo crontab -e
```

Füge die folgende Zeile hinzu, um Certbot jeden Tag um 2 Uhr morgens auszuführen:

```bash
0 2 * * * /usr/bin/certbot renew --quiet
```

### Schritt 6: Teste die SSL-Verbindung

Starte deine Flask-Anwendung und teste die SSL-Verbindung:

```bash
curl -k https://baettig.org:5000/api/test
```

### Schritt 7: (Optional) Verwende einen Reverse Proxy

Es wird empfohlen, einen Reverse Proxy wie Nginx oder Apache zu verwenden, um die SSL-Verbindung zu verwalten und die Flask-Anwendung im Hintergrund auszuführen. Dies kann die Leistung und Sicherheit deiner Anwendung verbessern.

### Zusammenfassung

1. Installiere Certbot.
2. Erhalte ein SSL-Zertifikat mit Certbot.
3. Konfiguriere deine Flask-Anwendung, um das Zertifikat zu verwenden.
4. Automatisiere die Erneuerung des Zertifikats.
5. Teste die SSL-Verbindung.

Wenn du Fragen hast oder auf Probleme stößt, lass es mich wissen!
