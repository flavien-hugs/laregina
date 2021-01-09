# accounts/middleware.py

class UserProfileMiddleware(object):
    """
        Ajoute le profil de l'utilisateur actuel à la demande, ou une fausse valeur pour les utilisateurs anonymes.
        Cette valeur doit être supérieure à celle de tout autre logiciel intermédiaire qui dépend de ces informations.
    """

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        # Ajouter le UserProfile actuel à la demande
        if request.user.is_anonymous or request.user.is_superuser:
            request.user = None
        else:
            request.user = request.user.is_buyer

        return self.get_response(request)