from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
import os
import json

# Anleitung für erstellen der Credentials siehe unten!
# Die Credentials müssen heruntergeladen und als credentials.json gespeichert werden


# Die Gmail API Scopes (Wir möchten E-Mails lesen)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    """Authentifiziert sich mit der Gmail API."""
    creds = None
    # Überprüfe, ob es Token gibt, die schon existieren (bereits authentifiziert)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Wenn keine gültigen Anmeldeinformationen vorhanden sind, logge dich ein
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Speichere die Anmeldeinformationen für das nächste Mal
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def search_emails(service, query):
    """Sucht nach E-Mails, die mit der Abfrage (query) übereinstimmen."""
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    if not messages:
        print("Keine Nachrichten gefunden.")
        return []
    print(f"{len(messages)} Nachrichten gefunden.")
    return messages

def get_email_content(service, msg_id):
    """Lädt den Inhalt einer E-Mail herunter."""
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    msg_data = message['payload']['headers']
    for d in msg_data:
        if d['name'] == 'Subject':
            subject = d['value']
    # Den Haupttextkörper dekodieren
    parts = message['payload'].get('parts', [])
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                return body
    return None

if __name__ == '__main__':
    # Authentifizieren
    service = gmail_authenticate()

    # Definiere den Suchbegriff (z.B. E-Mails mit einem bestimmten Betreff)
    search_query = 'subject:Kurze Nachfrage zu AI Seminar'
    
    # Suche nach E-Mails, die mit dem Betreff übereinstimmen
    messages = search_emails(service, search_query)

    # Lade die E-Mails herunter und zeige den Inhalt
    for msg in messages:
        msg_id = msg['id']
        content = get_email_content(service, msg_id)
        if content:
            print(f"Inhalt der Nachricht:\n{content}")

def gmail_search(query):
    service = gmail_authenticate()

    # Suche nach E-Mails, die mit dem Betreff übereinstimmen
    messages = search_emails(service, query)
    results = []
    
    # Lade die E-Mails herunter und zeige den Inhalt
    for msg in messages:
        msg_id = msg['id']
        content = get_email_content(service, msg_id)
        if content:
            results.append(content)
    
    return results

'''
Kein Problem! Ich erkläre dir Schritt für Schritt, wie du die `credentials.json` für die Verwendung der Gmail API generieren kannst.

### Schritte zum Erstellen der `credentials.json`:

1. **Gehe zur Google Cloud Console:**
   - Öffne [console.cloud.google.com](https://console.cloud.google.com/).

2. **Ein neues Projekt erstellen:**
   - Falls du noch kein Projekt hast, klicke oben links auf den Projektauswahl-Button und dann auf "Neues Projekt".
   - Gib dem Projekt einen Namen und klicke auf "Erstellen".

3. **Die Gmail API aktivieren:**
   - Nachdem dein Projekt erstellt wurde, klicke im linken Menü auf **"APIs & Dienste"** → **"Bibliothek"**.
   - Suche nach **Gmail API** in der Suchleiste und klicke darauf.
   - Klicke auf **"Aktivieren"**, um die Gmail API für dein Projekt zu aktivieren.

4. **Anmeldedaten (credentials) erstellen:**
   - Gehe zu **"APIs & Dienste"** → **"Anmeldedaten"** im linken Menü.
   - Klicke auf die Schaltfläche **"Anmeldedaten erstellen"** oben.
   - Wähle **"OAuth 2.0-Client-ID"**.

5. **OAuth-Zustimmung einrichten:**
   - Du wirst aufgefordert, einen **OAuth-Zustimmungsbildschirm** einzurichten. Klicke auf **"Zustimmungsbildschirm konfigurieren"**.
   - Wähle **"Extern"** aus, damit du mit deinem persönlichen Konto darauf zugreifen kannst, und klicke auf "Erstellen".
   - Fülle die grundlegenden Informationen aus (App-Name, E-Mail-Adresse) und klicke auf "Speichern und fortfahren".
   - Es ist nicht erforderlich, andere Informationen wie "Scopes" oder "Testbenutzer" hinzuzufügen. Klicke einfach auf "Speichern und fortfahren" bis zum Ende.

6. **OAuth-Client-ID erstellen:**
   - Nachdem du den Zustimmungsbildschirm eingerichtet hast, kehre zur Anmeldedaten-Seite zurück und klicke erneut auf **"Anmeldedaten erstellen"** → **"OAuth-Client-ID"**.
   - Wähle **"Desktop-App"** als Anwendungstyp.
   - Gib der Anwendung einen Namen (z.B. "Python Gmail API").
   - Klicke auf **"Erstellen"**.

7. **credentials.json herunterladen:**
   - Nach der Erstellung wird dir die **OAuth-Client-ID** angezeigt. Klicke auf **"Herunterladen"**, um die `credentials.json` Datei auf deinen Computer zu speichern.
   - Diese Datei enthält die Informationen, die Python benötigt, um auf die Gmail API zuzugreifen.

8. **Die `credentials.json` in dein Python-Projekt einbinden:**
   - Speichere die `credentials.json` Datei im selben Verzeichnis wie dein Python-Skript.

### Beispiel:
Dein Projektverzeichnis könnte so aussehen:
```
my_project/
│
├── credentials.json
└── download_emails.py  # Dein Python-Skript
```

Jetzt kannst du dein Python-Skript mit der Gmail API ausführen. Wenn du das Skript zum ersten Mal ausführst, wirst du zur Anmeldung bei deinem Google-Konto weitergeleitet, und ein OAuth-Token wird erstellt und gespeichert (in der `token.json` Datei). Dies ist nötig, um die Gmail API zu authentifizieren und E-Mails zu lesen.

### Häufige Fehler:
- **Zwei-Faktor-Authentifizierung**: Wenn du die Zwei-Faktor-Authentifizierung aktiviert hast, wird dieser Prozess dennoch funktionieren, da OAuth verwendet wird. Für direkte IMAP/SMTP-Zugriffe benötigst du jedoch ein App-Passwort, wie in der IMAP-Methode erwähnt.

Mit dieser Anleitung solltest du in der Lage sein, die `credentials.json` zu erstellen und die Gmail API für dein Python-Skript zu verwenden!
'''