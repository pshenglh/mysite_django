from django.shortcuts import render, redirect
from .models import Blog, Relatinship
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import LoginForm, SignUpForm, BlogForm
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

        return render(request, 'edit_blog.html', {'form':form, 'blog':blog})
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

class UserDetail(object):
    '''
    用户详细信息的类，根据实例化时传入的id查询文章信息和关注信息
    '''

    def __init__(self, user_id):
        self.id = user_id

    def blog_set(self):
        blog_set = Blog.objects.filter(author_id=self.id).order_by('-pub_date')
        return blog_set

    def blog_num(self):
        blog_set = self.blog_set()
        blog_num = len(blog_set)
        return blog_num

    def followed(self):
        relationship_set = Relatinship.objects.filter(follower_id=self.id)
        followed_set = []
        for relationship in relationship_set:
            followed_set.append(User.objects.get(id=relationship.followed_id))
        return followed_set

    def follower(self):
        relationship_set = Relatinship.objects.filter(followed_id=self.id)
        follower_set = []
        for relationship in relationship_set:
            follower_set.append(User.objects.get(id=relationship.follower_id))
        return follower_set

def user_detail(request, user_id):
    user_detail = UserDetail(user_id)
    return render(request, 'user_detail.html', {'user_detail':user_detail})

#关注他人
def follow_to(request, user_id):
    #在数据库中获取登录者的关系表
    relationship_exist_set = Relatinship.objects.filter(followed_id=request.user.id)
    follower = []
    for relationship_exist in relationship_exist_set:
        user = User.objects.get(id=relationship_exist.follower_id)
        follower.append(user.id)
    #检查是否已关注目标，若没关注这添加关注关系到数据库中
    #若已关注则返回提示
    if int(user_id) not in follower:
        relationship = Relatinship(
            followed=request.user,
            follower=User.objects.get(id=user_id)
        )
        relationship.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('Already followed')

