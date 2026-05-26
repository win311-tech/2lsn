from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('About/', views.About, name='about'),
    path('Shop/', views.Shop, name='shop'),
    path('Register/', views.Register, name='register'),
    path('Login/', views.Login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('checkout/', views.checkout, name='checkout'),

]

