# core/context.py

import os
import sys

def profile(request):
    
    # Ajoute le UserProfile (ou une valeur Falsy pour les utilisateurs anonymes) au contexte.
    # See: UserProfileMiddleware
    
    return {'profile': request.user}
