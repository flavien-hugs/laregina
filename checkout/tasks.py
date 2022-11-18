from django.conf import settings

import requests
from core.celery import app as celery_app
from checkout.models import Order, OrderItem

SENDER_ID = settings.SENDER_ID
SMS_API_KEY = settings.SMS_API_KEY


@celery_app.task(name="send_sms_order")
def send_sms_order(order_id):

    order = Order.objects.get(transaction_id=order_id)
    DESTINATAIRE = order.get_phone_number()
    NUMBER_TRANSACTION = order.get_order_id()
    MESSAGE = f"Bonjour, votre commande {NUMBER_TRANSACTION} a été validée avec succès. Merci pour votre achat sur LaRegina."

    SEND_SMS_URL = f"https://sms.lws.fr/sms/api?action=send-sms&api_key={SMS_API_KEY}&to={DESTINATAIRE}&from={SENDER_ID}&sms={MESSAGE}"

    response = requests.post(SEND_SMS_URL)
    return response.json()
