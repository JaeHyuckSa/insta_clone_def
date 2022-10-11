from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signin/',views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
]
