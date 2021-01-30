from django.urls import re_path
from apps.Nodes.views import main_page, index, node_view, port_view
from apps.Nodes.views import node_list, port_list
from apps.Nodes.views import node_edit, port_edit

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newNode$', node_view, name='newNode'),
	re_path(r'^newPort$', port_view, name='newPort'),
	re_path(r'^listNode$', node_list, name='listNode'),
	re_path(r'^listPort$', port_list, name='listPort'),
	re_path(r'^editNode/(?P<pk>[\w|\W]+)/$', node_edit, name='editNode'),
	re_path(r'^editPort/(?P<pk>[\w|\W]+)/$', port_edit, name='editPort'),
]