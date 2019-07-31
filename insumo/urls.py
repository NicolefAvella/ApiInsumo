from django.urls import path
from .views import ListInsumosView, LoginView, RegisterUsersView


urlpatterns = [
    path('insumos/', ListInsumosView.as_view(), name="insumos-all"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
]



