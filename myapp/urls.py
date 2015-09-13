from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^room/$', views.DetailRoomList.as_view(), name='detail_list'),
    url(r'^room/(?P<pid>[0-9]+)/$', views.room_detail, name='detail'),
    url(r'^room/thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^room/submit/$', views.submit_room, name='submit'),
    url(r'^room/find/$', views.find_room_from_key, name='find'),
    url(r'^room/edit/(?P<room_key>[^/]+)/$', views.submit_challenged, name='edit'),
    url(r'^room/error/$', TemplateView.as_view(template_name='room_ready_error.html'), name='room_ready_error'),
]