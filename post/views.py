# 리디렉션을 남발하면 서버 터진다...렌더는 한번 리디렉션은 여러번!
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from user.models import User

# Create your views here.
def index(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            context = dict()
            context['posts'] = Post.objects.all().order_by('-create_at')
            context['users'] = User.objects.all()
            return render(request, 'post/post/index.html', context=context)
        return render(request, 'post/post/index.html')

@login_required(login_url='/account/signin/')
def post_create(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'post/post/new_post.html')
        return render(request, 'account/user/login.html')
    
    elif request.method == 'POST':
        user = request.user
        image = request.FILES['image']
        content = request.POST.get('content')
        # 1. Post.objects.create로 만드는 법 2. Posts.save()로 만드는 법 
        Posts = Post.objects.create(author=user, image=image, content=content)
        return redirect('/')
    
# @login_required(login_url='/account/signin/')
# def post_delete(request, post_id):
#     if request.method ==