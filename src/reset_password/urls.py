from django.urls import path
from reset_password import views

urlpatterns = [
    path('activate/', views.activate_reset_password, name='activate_reset_password'),
    path('confirm/', views.reset_password_confirm, name='reset_password_confirm'),
]
