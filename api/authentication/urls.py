from django.urls import include, path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

auth_urls = [
    path('register/', views.UserRegistrationView.as_view()),
    path('change-login/', views.ChangeLoginView.as_view()), # Requires valid access token

    # Get token and refresh 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]