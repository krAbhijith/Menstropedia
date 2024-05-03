from django.urls import path
from .views import *

urlpatterns = [
    path('register/', AccountRegisterView.as_view(), name='register-account'),
    path('login/', AccountLoginView.as_view(), name='login-account'),
    path('logout/', AccountLogoutView.as_view(), name='logout-account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('tracker/', TrackerView.as_view(), name='tracker'),
    path('tolerate/', TrackerUpdateView.as_view(), name='tolerance'),
    path('correct/', TrackerCorrectView.as_view(), name='tracking-crct'),
]