from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'rooms', views.RoomSetView)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
	url(r'^room/', include(router.urls)),
    url(r'^getstarted/$', TemplateView.as_view(template_name='getting_started.html'), name='getstarted'),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^register/', views.register_user, name='register'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^bet/$', views.DetailRoomList.as_view(), name='detail_list'),
    url(r'^bet/(?P<pid>[0-9]+)/$', views.room_detail, name='detail'),
    url(r'^bet/thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^bet/submit/$', views.submit_room, name='submit'),
    url(r'^bet/find/$', views.find_room_from_key, name='find'),
    url(r'^bet/edit/(?P<room_key>[^/]+)/$', views.submit_challenged, name='edit'),
    url(r'^bet/error/$', TemplateView.as_view(template_name='room_ready_error.html'), name='room_ready_error'),
]