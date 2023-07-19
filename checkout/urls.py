from checkout import views
from django.urls import path


app_name = "checkout"
urlpatterns = [
    path(route="", view=views.show_checkout, name="checkout"),
    path(
        route="success/<int:order_id>",
        view=views.order_success_view,
        name="order_success",
    ),
    path(
        route="check/status-order/", view=views.track_order_view, name="order_tracking"
    ),
    path(
        route="download-invoice/<int:order_id>/",
        view=views.download_invoice_view,
        name="download_invoice",
    ),
]
