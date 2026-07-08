from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='api-login'),
    path('me', views.me, name='api-me'),
    path('logout', views.logout, name='api-logout'),
]
