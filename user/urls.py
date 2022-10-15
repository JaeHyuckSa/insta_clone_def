from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    #user
    path('signin/',views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    
    #profile
    path('users/<int:user_id>/', views.profile, name='profile'),
    path('edit-profile/<int:user_id>/', views.profile_update, name='profile-update'),
    
    #follow
    path('users/<int:user_id>/follow/', views.process_follow, name='process-follow'),
    path('users/<int:user_id>/followings/', views.following_list, name='following-list'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower-list'),
    path('users/recommend/', views.recommend_list, name='recommend-list'),
]
