# 리디렉션을 남발하면 서버 터진다...
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from user.models import User

# Create your views here.
def index(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            #값을 넘겨 줄떄는 사전형으로 만들어서 하면 깔끔하니 보기가 좋다.
            context = dict()
            context['posts'] = Post.objects.all().order_by('-create_at')
            context['users'] = User.objects.all()
            return render(request, 'post/post/index.html', context=context)


# def

#로그인이 한 사람만 접속이 가능하고 안되어있다면 로그인페이지로!
@login_required(login_url='/account/signin/')
def post_create(request):
    if request.method == 'GET':
        return render(request, 'post/post/new_post.html')
    
    elif request.method == 'POST':
        user = request.user
        #file을 불러올 때는 FILES['image']로 불러온다 
        image = request.FILES['image']
        content = request.POST.get('content')
        # 1. Post.objects.create로 만드는 법 2. Posts.save()로 만드는 법 
        #author=user도 넣어줘야 query가 비어지지 않는다. 항상 저장할 때는 생각하면서 작성
        Posts = Post.objects.create(author=user, image=image, content=content)
        return redirect('/')
    
@login_required(login_url='/account/signin/')
def post_delete(request, post_id):
    if request.method == 'GET':
        return  render(request, 'post/post/post_confirm_delete.html')
    
    elif request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('/')
    
@login_required(login_url='/account/signin/')
def post_update(request, post_id):
    if request.method == 'GET':
        context = dict()
        context['post'] = Post.objects.get(id=post_id)
        return render(request, 'post/post/edit_post.html', context=context)
    
    elif request.method == 'POST':
        #일단 연결되어있는 post_id랑 연결시켜야함 아니면 새로 생성됨...
        edit_post = Post.objects.get(id=post_id)
        edit_post.image = request.FILES['image']
        edit_post.content = request.POST.get('content')
        edit_post.save()
        return redirect('/')
    
        