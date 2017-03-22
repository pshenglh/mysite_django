from django.shortcuts import render, redirect
from .models import Blog, BlogForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import LoginForm, SignUpForm
from guardian.shortcuts import assign_perm, get_user_perms


# 首页处理视图函数
def index(request):
    blogs = Blog.objects.order_by('-mod_date')
    return render(request, 'index.html', {'blogs':blogs})

#博客详细页面
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog':blog})

#写文章
#@permission_required('blog.add_blog', login_url='/login/')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            #将提交的数据保存到数据库中
            blog = Blog(title=form.cleaned_data['title'],
                     body_text=form.cleaned_data['body_text'],
                     pub_date=timezone.now(),
                     mod_date=timezone.now(),
                     author=request.user)
            blog.save()
            #为新添加的文章分配修改和删除权限
            assign_perm('change_blog', request.user, blog)
            assign_perm('delete_blog', request.user, blog)
            return redirect('index')
    else:
        form = BlogForm()

    return render(request, 'add_blog.html', {'form':form})

#删除文章
def delete_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    if request.user.has_perm('delete_blog', blog):
        blog.delete()
        return redirect('index')
    else:
        return HttpResponse('Permission denied!')

#编辑文章
def edit_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    #测试对文章实例的修改权限
    if request.user.has_perm('change_blog', blog):
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
    else:
        return HttpResponse('Don\'t have the permission!')

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
            user.permissions.add('blog.add_blog')
            return HttpResponse('Sign up success!')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form':form})

