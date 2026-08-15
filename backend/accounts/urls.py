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

    path('hardware2026/board', views.Hardware2026BoardView.as_view(), name='api-hw2026-board'),
    path('hardware2026/months', views.Hardware2026MonthListCreateView.as_view(), name='api-hw2026-months-create'),
    path('hardware2026/months/<int:month_id>', views.Hardware2026MonthDetailView.as_view(), name='api-hw2026-month-detail'),
    path('hardware2026/months/<int:month_id>/records', views.Hardware2026RecordListCreateView.as_view(), name='api-hw2026-records-create'),
    path('hardware2026/records/<int:record_id>', views.Hardware2026RecordDetailView.as_view(), name='api-hw2026-record-detail'),
    path('hardware2026/preference', views.Hardware2026PreferenceView.as_view(), name='api-hw2026-preference'),
    path('hardware/overview', views.HardwareOverviewView.as_view(), name='api-hardware-overview'),
    path('hardware/tables', views.HardwareDynamicTableListCreateView.as_view(), name='api-hardware-tables'),
    path('hardware/tables/<int:table_id>', views.HardwareDynamicTableDetailView.as_view(), name='api-hardware-table-detail'),
    path('hardware/tables/<int:table_id>/rows', views.HardwareDynamicRowListCreateView.as_view(), name='api-hardware-table-rows'),
]