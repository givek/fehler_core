from django.urls import path

from . import views


urlpatterns = [
    path('register', views.RegisterUser.as_view(), name='create_user'),
    path('token', views.ObtainExpiringAuthToken.as_view(), name='token_obtain'),
    path('test', views.TestAuth.as_view(), name='test'),
]