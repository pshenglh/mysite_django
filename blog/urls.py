from  django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^delete/(?P<blog_id>[0-9]+)/$', views.delete_blog, name='delete'),
    url(r'^edit/(?P<blog_id>[0-9])+/$', views.edit_blog, name='edit'),
    url(r'(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add_blog/$', views.add_blog, name='add_blog'),
    url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up')
]