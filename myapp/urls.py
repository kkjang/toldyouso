from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^statement/$', views.DetailList.as_view(), name='detail_list'),
    url(r'^statement/(?P<pid>[0-9]+)/$', views.detail, name='detail'),
    url(r'^statement/thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^statement/submit/$', views.submit, name='submit'),
]