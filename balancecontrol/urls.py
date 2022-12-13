from django.urls import path

from . import views

app_name = 'balancecontrol'
urlpatterns = [
    path('', views.home, name='home'),
    path('createfinance/', views.createfinance, name='createfinance'),
]
