import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from credentials_anleitung import credentials_anleitung
import base64
import os
import json
from gpt import get_single_completion
from settings import MAX_EMAILS

# Anleitung für erstellen der Credentials siehe in credentials_anleitung.py
# Die Credentials müssen heruntergeladen und als credentials.json gespeichert werden

# Die Gmail API Scopes (Wir möchten E-Mails lesen)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    """Authentifiziert sich mit der Gmail API."""
    try:
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
    except Exception as e:
        print(f"Authentifizierung fehlgeschlagen: {e}")
        print(f"Stelle sicher, dass die `credentials.json` Datei im selben Verzeichnis wie dieses Skript liegt.")
        print(credentials_anleitung)
        return None

def search_emails(service, query):
    try:
        """Sucht nach E-Mails, die mit der Abfrage (query) übereinstimmen."""
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        if not messages:
            print("Keine Nachrichten gefunden.")
            return []
        print(f"{len(messages)} Nachrichten gefunden.")
        if len(messages) > MAX_EMAILS:
            print(f"Es wurden mehr als {MAX_EMAILS} Nachrichten gefunden. Es werden nur die ersten {MAX_EMAILS} Nachrichten angezeigt.")
            messages = messages[:MAX_EMAILS]

        return messages
    except Exception as e:
        print(f"Nachrichtensuche fehlgeschlagen: {e}")
        return []

def get_email_content(service, msg_id):
    """Lädt den Inhalt einer E-Mail herunter."""
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    msg_data = message['payload']['headers']
    
    # Den Haupttextkörper dekodieren
    parts = message['payload'].get('parts', [])
    body = None
    html_body = None

    def extract_parts(parts):
        nonlocal body, html_body
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                msg_data.append({'name': 'Body', 'value': body})
                break
            elif part['mimeType'] == 'text/html':
                html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                msg_data.append({'name': 'HTML Body', 'value': html_body})
            elif part['mimeType'] == 'multipart/mixed':
                # Rekursiv die Teile von multipart/mixed extrahieren
                extract_parts(part['parts'])
            elif part['mimeType'] == 'multipart/alternative':
                # Rekursiv die Teile von multipart/alternative extrahieren
                extract_parts(part['parts'])

    # Teile extrahieren
    extract_parts(parts)

    msg= json.dumps(msg_data, indent=2)
    return msg
    

def gmail_search(query):
    service = gmail_authenticate()

    # Suche nach E-Mails, die mit dem Betreff übereinstimmen
    messages = search_emails(service, query)
    results = []
    parts = []
    
    max_len = 50000

    # Lade die E-Mails herunter und zeige den Inhalt
    for msg in messages:
        msg_id = msg['id']
        content = get_email_content(service, msg_id)
        if content:
            results.append(content)
        str_results = str(results)
        size = len(str_results)
        if size >= max_len:
            print("Komprimiere Ergebnisse..."+str(len(parts)+1))
            part = get_single_completion("Komprimiere die folgenden Daten, entferne unnötige Informationen und formatierungen und wandle sie in Markdown um: ----data----\n" + str_results)
            sizenew = len(str(part))
            print("   Komprimierungfaktor: "+str(sizenew/size))
            parts.append(part)
            results = []

    if results:
        str_results = str(results)
        print("Komprimiere Ergebnisse..."+str(len(parts)+1))
        part = get_single_completion("Komprimiere die folgenden Daten, entferne unnötige Informationen und formatierungen und wandle sie in Markdown um: ----data----\n" + str_results)
        parts.append(part)  

    retval = json.dumps(parts)      
    
    return retval
