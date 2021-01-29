# order.cinetpay.py

import http
import urllib
from core import settings


def do_auth_capture(amount='0'):
	
	"""
	Une fonction qui se connecte à cinetpay avec les informations de facturation.
	Renvoie une liste Python contenant les paramètres de réponse de renvoyés
	par la passerelle de paiement. Le premier élément de la liste
	de réponse est le code de réponse; le 7ème élément est l'identifiant
	unique de la transaction
	"""

	raw_params = {'amount': amount}

	params = urllib.parse.urlencode(raw_params)
	cn = http.client.HTTPSConnection(settings.CINETPAY_POST_URL).request('POST', params)

	return cn
