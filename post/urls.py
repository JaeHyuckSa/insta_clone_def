from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('',views.index, name='index'),
    path('post/create/',views.post_create, name='post-create'),
    # path('post/<int:post_id>/delete/', views.post_delete, name='post-delete'),
]
