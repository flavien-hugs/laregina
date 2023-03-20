from django.conf import settings

import requests
from core.celery import app as celery_app
from checkout.models import Order, OrderItem

SENDER_ID = settings.SENDER_ID
SMS_API_KEY = settings.SMS_API_KEY
SMS_API_TOKEN = settings.API_TOKEN


@celery_app.task(name="send_sms_order")
def send_sms_order(order_id):

    order = Order.objects.get(transaction_id=order_id)
    DESTINATAIRE = order.get_phone_number()
    NUMBER_TRANSACTION = order.get_order_id()
    MESSAGE = f"Bonjour, votre commande {NUMBER_TRANSACTION} a été validée avec succès. Merci pour votre achat sur LaRegina."

    SEND_SMS_URL = f"https://panel.smsing.app/smsAPI?sendsms&apikey={SMS_API_KEY}&apitoken={SMS_API_TOKEN}&type=sms&from={SENDER_ID}&to={DESTINATAIRE}&text={MESSAGE}"

    response = requests.request("POST", SEND_SMS_URL)
    return response.json()
