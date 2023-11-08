from django.urls import path

from secret.apps import SecretConfig
from secret.views import (
    SecretListView, SecretGenerateView, SecretRetrieveView, SecretDestroyView, ReadSecretRetrieveView,
)

app_name = SecretConfig.name

urlpatterns = [
    path('', SecretListView.as_view(), name='secret-list'),
    path('generate/', SecretGenerateView.as_view(), name='secret-create'),
    path('<int:pk>/', SecretRetrieveView.as_view(), name='secret-retrieve'),
    path('delete/<int:pk>/', SecretDestroyView.as_view(), name='secret-destroy'),

    path('<str:secret_key>/', ReadSecretRetrieveView.as_view(), name='secret-show-url')
]
