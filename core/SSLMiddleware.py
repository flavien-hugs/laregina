# core.sslmiddleware.py

__license__ = "Python"
__copyright__ = "Copyright (C) 2007, Stephen Zabel"
__author__ = "Stephen Zabel - sjzabel@gmail.com"
__contributors__ = "Jay Parlar - parlar@gmail.com"

import RuntimeError
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, get_host

SSL = 'SSL'

class SSLRedirect:

    """
    classe de middleware pour la gestion des redirections entre
    les pages sécurisées et non sécurisées.
    Taken from: http://www.djangosnippets.org/snippets/880/
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False

        if not secure == self._is_secure(request):
            return self._redirect(request, secure)

    def _is_secure(self, request):
        if request.is_secure():
            return True

        # Gérer l'affaire Webfaction jusqu'à ce qu'elle soit résolue dans la requête .is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'
        return False

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        newurl = "{}://{}{}".format(self.protocol, self.get_host(request), self.request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            pass

        return HttpResponsePermanentRedirect(newurl)
