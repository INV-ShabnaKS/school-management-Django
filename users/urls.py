from django.urls import path
#from .views import RegisterView
from .views import LoginView
from .views import LogoutView


urlpatterns = [
    #path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
