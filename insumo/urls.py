from django.urls import path
from .views import ListInsumosView


urlpatterns = [
    path('insumos/', ListInsumosView.as_view(), name="insumos-all")
]