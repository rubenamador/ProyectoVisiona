from django.urls import re_path
from apps.Nodes.views import main_page, index, node_view, port_view
from apps.Nodes.views import node_list, port_list
from apps.Nodes.views import node_edit, port_edit, node_delete, port_delete
from apps.Nodes.views import NodeList, PortList, NodeCreate, PortCreate

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newNode$', NodeCreate.as_view(), name='newNode'),
	re_path(r'^newPort$', PortCreate.as_view(), name='newPort'),
	re_path(r'^listNode$', NodeList.as_view(), name='listNode'),
	re_path(r'^listPort$', PortList.as_view(), name='listPort'),
	re_path(r'^editNode/(?P<pk>[\w|\W]+)/$', node_edit, name='editNode'),
	re_path(r'^editPort/(?P<pk>[\w|\W]+)/$', port_edit, name='editPort'),
	re_path(r'^deleteNode/(?P<pk>[\w|\W]+)/$', node_delete, name='deleteNode'),
	re_path(r'^deletePort/(?P<pk>[\w|\W]+)/$', port_delete, name='deletePort'),
]