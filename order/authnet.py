# order.authnet.py


import http
import urllib
from core import settings


def do_auth_capture(amount='0', card_num=None, exp_date=None, card_cvv=None):

  """
    une fonction qui se connecte à authorize.net avec les informations de facturation.
    Renvoie une liste Python contenant les paramètres de réponse de renvoyés
    par la passerelle de paiement. Le premier élément de la liste des réponses
    est le code de réponse; le 7ème élément est l'identifiant unique de la transaction
  """

  delimiter = '|'
  raw_params = {
    'x_login': settings.AUTHNET_LOGIN,
    'x_tran_key': settings.AUTHNET_KEY,
    'x_type': 'AUTH_CAPTURE',
    'x_amount': amount,
    'x_version': '3.1',
    'x_card_num': card_num,
    'x_exp_date': exp_date,
    'x_delim_char': delimiter,
    'x_relay_response': 'FALSE',
    'x_delim_data': 'TRUE',
    'x_card_code': card_cvv
  }

  params = urllib.parse.urlencode(raw_params)

  headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'content-length': len(params)
  }

  post_url = settings.AUTHNET_POST_URL
  post_path = settings.AUTHNET_POST_PATH

  cxt = http.client.HTTPSConnection(
    post_url,
    http.client.HTTPS_PORT
  )

  cxt.request(
    'POST',
    post_path,
    params,
    headers
  )

  return cxt.getresponse().read().decode()
