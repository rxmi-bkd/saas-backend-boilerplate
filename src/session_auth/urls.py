from django.urls import path
from session_auth import views

urlpatterns = [
    path('register/', views.register, name='session_register'),
    path('login/', views.login, name='session_login'),
    path('logout/', views.logout, name='session_logout'),
    path('update/password/', views.update_password, name='session_update_password'),
    path('update/user/', views.update_user, name='session_update_user'),
    path('whoami/', views.who_am_i, name='session_whoami'),
]
