from django.urls import path
from .views import ListInsumosView, LoginView, RegisterUsersView, InsumosDetailView


urlpatterns = [
    path('insumos/', ListInsumosView.as_view(), name="insumos-list-create"),
    path('insumos/<int:pk>/', InsumosDetailView.as_view(), name="insumos-detail"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
]
