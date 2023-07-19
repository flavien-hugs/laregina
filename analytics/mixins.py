# analytics/mixins.py
from analytics.signals import object_viewed_signal


class ObjectViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        instance = context.get("object")
        if instance:
            object_viewed_signal.send(
                instance.__class__, instance=instance, request=self.request
            )
        return context
