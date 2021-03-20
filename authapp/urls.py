from django.urls import path

from authapp.views import login, RegisterCreateView, logout, ProfileUpdateView


app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]