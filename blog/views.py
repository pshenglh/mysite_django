from django.shortcuts import render
from django.http import request, HttpResponse
from .models import Blog, BlogForm, Author
from django.shortcuts import get_object_or_404
from django.utils import timezone

# 首页处理视图函数
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs':blogs})

#博客详细页面
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog':blog})

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            b = Blog(title=form.cleaned_data['title'],
                     body_text=form.cleaned_data['body_text'],
                     pub_date=timezone.now(),
                     mod_date=timezone.now(),
                     author=Author.objects.get(pk=1))
            b.save()
            render(request, 'index.html')
    else:
        form = BlogForm()

    return render(request, 'addblog.html', {'form':form})