from  django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add_blog/$', views.add_blog, name='add_blog'),
]