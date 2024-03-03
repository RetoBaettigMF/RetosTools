import requests
import json

TEAMS_HOOK = "https://mfeng.webhook.office.com/webhookb2/dc1e3b78-9986-4199-b0a2-48aa375a0424@7e35793e-43c3-40a6-abde-65b56160d26a/IncomingWebhook/171a968ce0674c4c9136fc558ab015bd/a5c82cf7-fad1-42e5-97bc-baaf2b0a1f81"

def send_teams_message(title, message):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        '@context': 'https://schema.org/extensions',
        '@type': 'MessageCard',
        'title': title,
        'text': message
    }
    response = requests.post(TEAMS_HOOK, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise ValueError(
            'Anfrage an Teams gesendet, aber fehlgeschlagen: Rückgabecode={}, Antwort={}'.format(
            response.status_code, response.text
            )
        )
    print("Message sent to Teams")