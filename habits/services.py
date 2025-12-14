import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    """ отправляет сообщение в телеграм """
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'
    response = requests.post(url, data=params)
    return response.json()
