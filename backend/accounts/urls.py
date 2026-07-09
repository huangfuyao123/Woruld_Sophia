from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='api-login'),
    path('me', views.me, name='api-me'),
    path('logout', views.logout, name='api-logout'),
    path('profile', views.update_profile, name='api-profile'),
    path('change-password', views.change_password, name='api-change-password'),
    path('accounts', views.account_list, name='api-accounts-list'),
    path('accounts/create', views.account_create, name='api-accounts-create'),
    path('accounts/<int:pk>/update', views.account_update, name='api-accounts-update'),
    path('accounts/<int:pk>/delete', views.account_delete, name='api-accounts-delete'),
    path('generate-password', views.generate_pwd, name='api-generate-password'),
]
