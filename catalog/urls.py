from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='Confirences'),
    path('More_details/<int:id>/', views.More_info, name='More_info'),
    path('register/', views.RegisterUser, name='register_user'),
    path('login/', views.LoginToAccount, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('register_confirence/<int:id>/', views.RegisterOnConfirence, name='register_on_confirence'),
    path('change_password/', views.ChangePassword, name='change_password'),
    path('activate/<str:hashuser>', views.activate, name='activate'),


]
