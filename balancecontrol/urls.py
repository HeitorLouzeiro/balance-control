from django.urls import path

from . import views

app_name = 'balancecontrol'
urlpatterns = [
    path('', views.home, name='home'),
    path('createfinance/', views.createfinance, name='createfinance'),
    path('editfinance/', views.editfinance, name='editfinance'),
    path('deletefinance/', views.deletefinance, name='deletefinance'),
]
