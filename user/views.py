from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from django.contrib.auth import get_user_model 
# Create your views here.

def signin(request):
    if request.method == 'POST':
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
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/account/login.html')

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
            if email == '' or username == '' or password == '':
                return render(request, 'user/account/signup.html', {'error': '이메일과 사용자 이름과 패스워드는 필수 값입니다.'})

            exist_user = User.objects.filter(email=email, username=username)
            if exist_user:
                return render(request, 'user/account/signup.html', {'error': '이메일과 사용자이름이 이미 존재합니다. '})
            else:
                User.objects.create_user(email=email, username=username, password=password)
                return redirect('/account/signin/')