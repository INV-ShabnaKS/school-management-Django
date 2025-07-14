from django.urls import path
#from .views import RegisterView
from .views import LoginView
from .views import LogoutView
from .views import RequestPasswordResetEmail
from .views import PasswordResetConfirmView


urlpatterns = [
    #path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('reset-password/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    ]
