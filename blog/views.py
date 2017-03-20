from django.shortcuts import render, redirect
from .models import Blog, BlogForm, Author
from django.shortcuts import get_object_or_404
from django.utils import timezone


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
                     author=Author.objects.get(pk=1))
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