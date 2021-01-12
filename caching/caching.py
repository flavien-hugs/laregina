# caching.caching.py

from django.core.cache import cache
from core.settings import CACHE_TIMEOUT

def cache_update(sender, **kwargs):
    """ pour mettre à jour une instance de modèle dans le cache;
        toute classe de modèle utilisant ce signal doit avoir une propriété "cache_key" d'identification unique. 
    """

    item = kwargs.get('instance')
    cache.set(item.cache_key, item, CACHE_TIMEOUT)
    
def cache_evict(sender, **kwargs):
    """ pour mettre à jour une instance de modèle dans le cache;
        toute classe de modèle utilisant ce signal doit avoir une propriété "cache_key" d'identification unique. 
    """

    item = kwargs.get('instance')
    cache.delete(item.cache_key)

