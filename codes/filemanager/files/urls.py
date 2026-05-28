from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^browse/(?P<rel_path>.+)/$', views.browse, name='browse'),
    path('browse/', views.browse, name='browse_root'),
    re_path(r'^preview/(?P<rel_path>.+)$', views.preview, name='preview'),
    re_path(r'^edit/(?P<rel_path>.+)$', views.edit, name='edit'),
    re_path(r'^download/(?P<rel_path>.+)$', views.download, name='download'),
]
