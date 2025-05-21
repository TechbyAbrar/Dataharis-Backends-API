from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('get_user_profile/', views.user_profile, name='get_user_profile'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('update_password/', views.update_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('logout/', views.logout, name='logout'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('dashboardView/', views.dashboardView, name='dashboardView'),
    path('specific-user/<int:pk>/', views.specific_user, name='specific_user'),
    # SOCAIL AUTH
    path('googleLogin/', views.GoogleLoginAPIView.as_view(), name='google-login'),
    path('facebookLogin/', views.FacebookLoginAPIView.as_view(), name='facebook-login'),
    
]
