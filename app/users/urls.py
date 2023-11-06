from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    UsersListView, UsersRegistrationView,
    UsersRetrieveView, UsersUpdateView, UsersVerifyEmailView,
    UsersDestroyView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('', UsersListView.as_view(), name='users-list'),
    path('create/', UsersRegistrationView.as_view(), name='users-create'),
    path('<int:pk>/', UsersRetrieveView.as_view(), name='user-retrieve'),
    path('update/<int:pk>/', UsersUpdateView.as_view(), name='users-update'),
    path('delete/<int:pk>/', UsersDestroyView.as_view(), name='users-destroy'),

    path(
        'verify_email/<uidb64>/<token>/',
        UsersVerifyEmailView.as_view(),
        name='verify-email'
    ),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
