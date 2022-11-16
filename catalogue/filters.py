# catalogue.filter.py

from django.core.exceptions import ImproperlyConfigured


class FilterMixin(object):
    filter_class = None
    search_ordering_param = "ordering"

    def get_queryset(self, *args, **kwargs):
        try:
            qs = super().get_queryset(*args, **kwargs)
            return qs
        except Exception:
            raise ImproperlyConfigured(
                "Vous devez disposer d'un queryset pour \
                pouvoir utiliser le FilterMixin"
            )

    def get_context_data(self, *args, **kwargs):
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs = qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f = filter_class(self.request.GET, queryset=qs)
            kwargs["object_list"] = f
        return super().get_context_data(*args, **kwargs)
