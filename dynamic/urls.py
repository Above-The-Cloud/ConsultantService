
from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    url(r'^create$', views.create),
    url(r'^createComment$', views.createComment),
    url(r'^createReply$', views.createReply),
    url(r'^update$', views.update),
    url(r'^delete$', views.delete),
    url(r'^deleteComment$', views.deleteComment),
    url(r'^deleteReply$', views.deleteReply),
    url(r'^list$', views.list),
    url(r'^listComment$', views.listComment),
    url(r'^listReply$', views.listReply),
]