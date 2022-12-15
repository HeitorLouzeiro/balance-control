from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('reset_password/', views.resetPassword, name='resetPassword'),  # ok
    path('reset_password_sent/', views.resetPasswordSent,
         name='resetPasswordSent'),  # ok
    path('reset/<uidb64>/<token>/', views.resetPasswordConfirm,
         name='resetPasswordConfirm'),  # ok
    path('reset_password_complete/', views.resetPasswordComplete,
         name='resetPasswordComplete'),
]
