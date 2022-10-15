from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    #post
    path('', views.index, name='index'),
    path('post/all/', views.all_post, name='all-post'),
    path('post/<int:post_id>/detail/', views.post_detail, name='post-detail' ),
    path('post/create/', views.post_create, name='post-create'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post-delete'),
    path('post/<int:post_id>/edit/', views.post_update, name='post-update'),
    
    #comment
    path('comment/<int:comment_id>/create/', views.comment_create, name='comment-create'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment-delete'),
    path('comment/<int:comment_id>/edit/', views.comment_update, name='comment-update'),
    
    #profile
    path('users/<int:user_id>/', views.profile, name='profile'),
    path('edit-profile/<int:user_id>/', views.profile_update, name='profile-update'),
    path('users/<int:user_id>/likeed_list/', views.liked_list, name='liked-list'),

    
    #like
    path('post/<int:post_id>/likes/', views.likes, name='likes'),
    
    #follow
    path('users/<int:user_id>/follow/', views.process_follow, name='process-follow'),
    path('users/<int:user_id>/followings/', views.following_list, name='following-list'),
    path('users/<int:user_id>/followers/', views.follower_list, name='follower-list'),
    path('users/recommend/', views.recommend_list, name='recommend-list'),
]
