from django.urls import re_path
from apps.Links.views import main_page, index, link_view
from apps.Links.views import link_list
from apps.Links.views import link_edit, link_delete
from apps.Links.views import LinkList, LinkCreate, LinkUpdate, LinkDelete
from apps.Links.views import LinkGraph, LinkConnect, LinkPath
from apps.Links.views import LinkAPI
from apps.Links.views import all_links_delete, all_links_update

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newLink$', LinkCreate.as_view(), name='newLink'),
	re_path(r'^listLink$', LinkList.as_view(), name='listLink'),
	re_path(r'^editLink/(?P<pk>[\w|\W]+)/$', LinkUpdate.as_view(), name='editLink'),
	re_path(r'^deleteLink/(?P<pk>[\w|\W]+)/$', LinkDelete.as_view(), name='deleteLink'),
	re_path(r'^apiLink$', LinkAPI.as_view(), name='apiLink'),
	re_path(r'^graphLink$', LinkGraph.as_view(), name='graphLink'),
	re_path(r'^connectLink/(?P<pk>[\w|\W]+)/$', LinkConnect.as_view(), name='connectLink'),
	re_path(r'^pathLink/(?P<pk>[\w|\W]+)/(?P<pk2>[\w|\W]+)/$', LinkPath.as_view(), name='pathLink'),
	re_path(r'^deleteAllLinks$', all_links_delete, name='deleteAllLinks'),
	re_path(r'^updateAllLinks$', all_links_update, name='updateAllLinks'),
]