# 리디렉션을 남발하면 서버 터진다...
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from user.models import User

# Create your views here.

def index(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            #값을 넘겨 줄떄는 사전형으로 만들어서 하면 깔끔하니 보기가 좋다. 
            # 또 다른 방법으로 넘겨 줄 수 있는데 context={ 'user': user} 이런식으로 가능하다.
            context = dict()
            context['users'] = User.objects.all()
            context['latest_following_post'] = Post.objects.filter(author__followers=request.user).order_by('-create_at')
            return render(request, 'post/post/index.html', context=context)
        return render(request, 'post/post/index.html')

#로그인이 한 사람만 접속이 가능하고 안되어있다면 로그인페이지로!
@login_required(login_url='user:signin')
def all_post(request):
    if request.method == 'GET':
        context = dict()
        context['posts'] = Post.objects.all()
        return render(request, 'post/post/all_post.html', context=context)

@login_required(login_url='user:signin')
def post_detail(request, post_id):
    if request.method == 'GET':
        context = dict()
        context['post'] = Post.objects.get(id=post_id)
        context['users'] = User.objects.all()
        #filter와 get의 차이를 확실히 알아야한다.최신순으로 불러오기!
        context['comments'] = Comment.objects.filter(post_id=post_id).order_by('-create_at')
        return render(request, 'post/post/post_detail.html', context=context)

@login_required(login_url='user:signin')
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
        Post.objects.create(author=user, image=image, content=content)
        return redirect('/')
    
@login_required(login_url='user:signin')
def post_delete(request, post_id):
    if request.method == 'GET':
        return  render(request, 'post/post/post_confirm_delete.html')
    
    elif request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('/')
    
@login_required(login_url='user:signin')
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
    
@login_required(login_url='user:signin')
def comment_create(request, comment_id):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(id=comment_id)
        content = request.POST.get('content')
        #comment = Comment() ->모델 불러오는 법
        #이렇게 하는 방식도 있지만 모델을 불러와서 comment.content = content 로 하는 방법으로 save하는 방식
        Comment.objects.create(content=content, author=user, post=post)
        #post_id와 post.id와 다른 것이다!!!!!!!!!!!!!!!!!
        return redirect('post:post-detail', post.id)
    
@login_required(login_url='user:signin')
def comment_delete(request, comment_id):
    if request.method == 'GET':      
        return render(request, 'post/post/comment_confirm_delete.html' )
    
    elif request.method == 'POST': 
        comment = Comment.objects.get(id=comment_id)
        post_id = comment.post.id
        comment.delete()

        return redirect('post:post-detail', post_id)
        
@login_required(login_url='user:signin')
def comment_update(request, comment_id):
    if request.method == 'GET':
        context = dict()
        context['comment'] = Comment.objects.get(id=comment_id)
        return render(request, 'post/post/comment_update_form.html', context=context)
    
    elif request.method =='POST':
        edit_comment = Comment.objects.get(id=comment_id)
        post_id = edit_comment.post.id
        edit_comment.content = request.POST.get('content')
        edit_comment.save()
        #디테일 페이지로 이동하는 방법 comment로 인자값을 가져온다!
        return redirect('post:post-detail', post_id) #redirect는 url 뿐만아니라 url name도 설정해줄 수 있다.
        #return redirect('/post/detail/'+str(post_id)) #장진님! 이런식으로 디테일 페이지로 이동할 수 있는 방법이 있다

@login_required(login_url='user:signin')
def likes(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)

        if post.like_authors.filter(id=request.user.id).exists(): 
            post.like_authors.remove(request.user)
        else:
            post.like_authors.add(request.user)
        return redirect(request.META['HTTP_REFERER']) #현재페이지로 리다이렉트 함!

@login_required(login_url='user:signin')
def liked_list(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['profile_user'] = User.objects.get(id=user_id)
        context["liked_posts"] = Post.objects.filter(like_authors=user_id)
        
        return render(request, 'post/post/post_like_list.html', context=context)

@login_required(login_url='user:signin')
def bookmarks(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)

        if post.bookmark_authors.filter(id=request.user.id).exists(): 
            post.bookmark_authors.remove(request.user)
        else:
            post.bookmark_authors.add(request.user)
        return redirect(request.META['HTTP_REFERER']) #현재페이지로 리다이렉트 함!

@login_required(login_url='user:signin')
def bookmarked_list(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['profile_user'] = User.objects.get(id=user_id)
        context["bookmarked_posts"] = Post.objects.filter(bookmark_authors=user_id)
        
        return render(request, 'post/post/post_bookmark_list.html', context=context)
