from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'rooms', views.RoomSetView)
router.register(r'wagers', views.WagerSetView)
router.register(r'bets', views.BetSetView)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
	url(r'^room/', include(router.urls)),
    url(r'^getstarted/$', TemplateView.as_view(template_name='getting_started.html'), name='getstarted'),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^register/', views.register_user, name='register'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^room/$', views.DetailRoomList.as_view(), name='detail_list'),
    url(r'^room/a/$', views.test_query_string, name='test-for-string'),
    url(r'^room/(?P<pid>[0-9]+)/$', views.room_detail, name='detail'),
    url(r'^room/thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    url(r'^room/submit/$', views.SubmitBetFormView.as_view(), name='submit'),
    url(r'^room/find/$', views.find_room_from_key, name='find'),
    url(r'^room/edit/(?P<room_key>[^/]+)/$', views.submit_challenged, name='edit'),
    url(r'^room/error/$', TemplateView.as_view(template_name='room_ready_error.html'), name='room_ready_error'),
]