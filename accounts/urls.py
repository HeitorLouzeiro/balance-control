from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('reset_password/', views.resetPassword, name='resetPassword'),
    path('reset_password_sent/', views.resetPasswordSent,
         name='resetPasswordSent'),
    path('reset', views.resetPasswordConfirm,
         name='resetPasswordConfirm'),
    path('reset_password_complete/', views.resetPasswordComplete,
         name='resetPasswordComplete'),
    path('invalid/', views.resetPasswordInvalid, name='resetPasswordInvalid'),
    path('expired/', views.resetPasswordExpired, name='resetPasswordExpired')
]
