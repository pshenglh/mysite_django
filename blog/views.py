from django.shortcuts import render, redirect
from .models import Blog, BlogForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm


# 首页处理视图函数
def index(request):
    blogs = Blog.objects.order_by('-mod_date')
    return render(request, 'index.html', {'blogs':blogs})

#博客详细页面
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog':blog})

#写文章
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            #将提交的数据保存到数据库中
            blog = Blog(title=form.cleaned_data['title'],
                     body_text=form.cleaned_data['body_text'],
                     pub_date=timezone.now(),
                     mod_date=timezone.now(),
                     author=User.objects.get(pk=1))
            blog.save()
            return redirect('index')
    else:
        form = BlogForm()

    return render(request, 'add_blog.html', {'form':form})

#删除文章
def delete_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    blog.delete()
    return redirect('index')

#编辑文章
def edit_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    data = {
        'title': blog.title,
        'body_text': blog.body_text
    }
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            #修改该文章被修改的部分并将提交的数据保存到数据库中
            blog.title = form.cleaned_data['title']
            blog.body_text = form.cleaned_data['body_text']
            blog.mod_date = timezone.now()
            blog.save()
            return redirect('index')
    else:
        form = BlogForm(data)

    return render(request, 'add_blog.html', {'form':form})

#登录
def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponse(request.user.username)
        else:
            return HttpResponse('ERROR')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form':form})

#登出
def my_logout(request):
    logout(request)
    return HttpResponse('logout success')

#注册
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid() and \
                form.cleaned_data['password'] == form.cleaned_data['password1']:
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            user.save()
            return HttpResponse('Sign up success!')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form':form})