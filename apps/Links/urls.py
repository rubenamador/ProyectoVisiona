from django.urls import re_path
from apps.Links.views import main_page, index, link_view
from apps.Links.views import link_list
from apps.Links.views import link_edit

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newLink$', link_view, name='newLink'),
	re_path(r'^listLink$', link_list, name='listLink'),
	re_path(r'^editLink/(?P<pk>[\w|\W]+)/$', link_edit, name='editLink'),
]