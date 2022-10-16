from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import User
from post.models import Post
from .validators import contains_special_character, contains_uppercase_letter, contains_lowercase_letter, contains_number


# Create your views here.
#template에서 값을 넘겨줄 때 input방식과 form방식이있다.
#template에서 input값으로 데이터 받아오는 방법이 있다
#forms.py를 만들어 필드를 정의한다음  form.is_valid를 사용하여 처리리하는 방법이 있다
#account
def signin(request):
    if request.method == 'GET':
        user = request.user.is_authenticated #bool값으로 True냐 False냐...
        if user:
            return redirect('/')
        else:
            return render(request, 'user/account/login.html')
        
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        username = User.objects.get(email=email)
        password = request.POST.get('password', '')
        me = auth.authenticate(request, username=username, password=password) 
        #authenticate를 오버라이딩해서 username을 email로 받을 수 있게 하는 방법이 있다! (정석 루트)
        if me is not None:  
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/account/login.html', {'error':'이메일 혹은 패스워드를 확인 해주세요.'})
    
def signup(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/account/signup.html')
    elif request.method == "POST":
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        if password != password2:
            return render(request, 'user/account/signup.html', {'error': '패스워드를 확인 해 주세요.'})
        else:
            if (len(password) < 8 
                or not contains_uppercase_letter(password)
                or not contains_lowercase_letter(password)
                or not contains_number(password) 
                or not contains_special_character(password) 
            ):
                return render(request, 'user/account/signup.html', {'error':'8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다.' })
            
            if email == '' or username == '' or password == '':
                return render(request, 'user/account/signup.html', {'error': '이메일과 사용자 이름과 패스워드는 필수 값입니다.'})

            email_exist_user = User.objects.filter(email=email)
            username_exist_user = User.objects.filter(username=username)
            if email_exist_user or username_exist_user :
                return render(request, 'user/account/signup.html', {'error': '이메일 또는 사용자이름이 이미 존재합니다. '})
            
            else:
                User.objects.create_user(email=email, username=username, password=password)
                return redirect('/account/signin/')
            
@login_required(login_url='user:signin')
def logout(request):
    auth.logout(request)
    return redirect('/account/signin/')

#follow
@login_required(login_url='user:signin')
def process_follow(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        if user != request.user:
            if user.followers.filter(id=request.user.id).exists():
                user.followers.remove(request.user)
            else:
                user.followers.add(request.user)
        return redirect(request.META['HTTP_REFERER'])
    
@login_required(login_url='user:signin')
def following_list(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['followings'] = User.objects.get(id=user_id).followings.all()
        context['profile_user_id'] = User.objects.get(id=user_id)
        return render(request, 'user/account/following_list.html', context=context)

@login_required(login_url='user:signin')
def follower_list(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['followers'] = User.objects.get(id=user_id).followers.all()
        context['profile_user_id'] = User.objects.get(id=user_id)
        return render(request, 'user/account/follower_list.html', context=context)
    
@login_required(login_url='user:signin')
def recommend_list(request):
    if request.method == 'GET':
        context = dict()
        context['recommends'] = User.objects.all()
        return render(request, 'user/account/recommend_list.html', context=context)

#profile
@login_required(login_url='user:signin')
def profile(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['profile_user'] = User.objects.get(id=user_id)
        context["user_post"] = Post.objects.filter(author=user_id)#author를 타고 user_id해야함

        return render(request, 'user/account/profile.html', context=context)

@login_required(login_url='user:signin')
def profile_update(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['user'] = User.objects.get(id=user_id)
        return render(request, 'user/account/profile_update_form.html', context=context)
    
    elif request.method == 'POST':
        edit_user = User.objects.get(id=user_id)
        edit_user.username = request.POST.get('username')
        edit_user.profile_image = request.FILES['image']
        edit_user.intro = request.POST.get('intro')
        edit_user.save()
        
        return redirect('user:profile', user_id)
    
