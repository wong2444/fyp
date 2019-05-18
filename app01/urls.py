from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('open_camera/', views.open_camera, name='open_camera'),
    path('t_history/', views.t_history, name='t_history'),
    path('s_history/', views.s_history, name='s_history'),

]
