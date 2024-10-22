
## Installation und start der Anwendung

**Installation**`

Die installation erstellt zuerst ein virtuelles environment uns installiert alle benötigten python pakete:
```
install.bat
```

**Starten die Anwendung:**

Setze zuerst die secrets in ..\setkey.bat. Minimal muss die Umgebungsvariable RETOS_API_TOKEN definiert sein.

```setkey.bat
@echo off
set RETOS_API_TOKEN=T3BlbkFJZIgqFQlv9BpZ1r8BiwjW
echo on
```
Zum starten muss das venv und dann der service gestartet werden.

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

**Reverse Proxy installieren**

Der Service muss nun noch uber einen Reverse Proxy erreichbar sein. 
Dazu wird ein Reverse Proxy wie [nginx](https://www.nginx.com/) 
benötigt. Für diesen muss dann über z.B. LetsEncrypt ein SSL Zertifikat
Installiert werden, damit der Service über 443 geschützt wird.

In Apache ist dafür folgender Eintrag in /etc/apache2/sites-enabled/000-default.conf zu machen:

```
# Weiterleitung von /rolx an Port 5000
ProxyPass /rolx http://localhost:5000/rolx
ProxyPassReverse /rolx http://localhost:5000/rolx
```