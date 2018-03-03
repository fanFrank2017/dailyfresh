from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^detail/$',views.detail),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.list),
    url(r'^(\d+)/$',views.detail),
]