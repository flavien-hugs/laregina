# core/context.py

import os
import sys

from core import settings
from core.customize import custome_vals


def customization(request):
    """
    Ajoute les variables de personnalisation à la demande.
    """

    # Vérifie que si un logo a été spécifié, le fichier existe.
    if custome_vals['custome_logo'] and not os.path.isfile(custome_vals['custome_logo_path']):
        sys.stderr("Erreur : Le fichier pour le logo n'existe pas à " + custome_vals['custome_logo_path'] + '\nUtiliser le logo texte à la place.')
        custome_vals['custome_logo'] = False
    return custome_vals


# HEAD META
def context(request):
    return {
        'title': settings.SITE_NAME,
        'desc': settings.INDEX_DESCRIPTION,
        'description': settings.SITE_DESCRIPTION,
        'keywords': settings.META_KEYWORDS,
        'facebook': 'https://www.facebook.com/laregina.ci/',
        'twitter': 'https://twitter.com/CoteLaregina',
        'request': request
    }


def user_profile(request):
    
    # Ajoute le UserProfile (ou une valeur Falsy pour les utilisateurs anonymes) au contexte.
    # See: UserProfileMiddleware
    
    return {'profile': request.profile}
