from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='api-login'),
    path('me', views.MeView.as_view(), name='api-me'),
    path('logout', views.LogoutView.as_view(), name='api-logout'),
    path('profile', views.ProfileView.as_view(), name='api-profile'),
    path('change-password', views.ChangePasswordView.as_view(), name='api-change-password'),
    path('accounts', views.AccountListView.as_view(), name='api-accounts-list'),
    path('accounts/create', views.AccountCreateView.as_view(), name='api-accounts-create'),
    path('accounts/<int:pk>/update', views.AccountUpdateView.as_view(), name='api-accounts-update'),
    path('accounts/<int:pk>/delete', views.AccountDeleteView.as_view(), name='api-accounts-delete'),
    path('generate-password', views.GeneratePasswordView.as_view(), name='api-generate-password'),
]
