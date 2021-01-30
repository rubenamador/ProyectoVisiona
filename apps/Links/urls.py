from django.urls import re_path
from apps.Links.views import main_page, index, link_view
from apps.Links.views import link_list
from apps.Links.views import link_edit, link_delete
from apps.Links.views import LinkList, LinkCreate, LinkUpdate

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newLink$', LinkCreate.as_view(), name='newLink'),
	re_path(r'^listLink$', LinkList.as_view(), name='listLink'),
	re_path(r'^editLink/(?P<pk>[\w|\W]+)/$', LinkUpdate.as_view(), name='editLink'),
	re_path(r'^deleteLink/(?P<pk>[\w|\W]+)/$', link_delete, name='deleteLink'),
]