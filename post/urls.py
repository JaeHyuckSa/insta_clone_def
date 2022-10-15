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
    
    #like
    path('post/<int:post_id>/likes/', views.likes, name='likes'),
    path('users/<int:user_id>/liked_list/', views.liked_list, name='liked-list'),
    
    #bookmark
    path('post/<int:post_id>/bookmarks/', views.bookmarks, name='bookmarks'),
    path('users/<int:user_id>/bookmarked_list/', views.bookmarked_list, name='bookmarked-list'),

]
