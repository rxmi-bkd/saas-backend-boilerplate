from django.urls import path

from session_auth import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/password/', views.update_password, name='update_password'),
    path('update/user/', views.update_user, name='update_user'),
    path('whoami/', views.who_am_i, name='whoami'),
]
