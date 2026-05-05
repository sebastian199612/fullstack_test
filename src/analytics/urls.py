from django.urls import path

from analytics import views
from django.urls import path
from .views import SalesView

urlpatterns = [
    path("sales", views.SalesView.as_view(), name="sales-analytics"),
    path('ventas/', SalesView.as_view(), name='sales-analytics'),
    ]
