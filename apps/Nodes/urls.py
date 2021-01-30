from django.urls import re_path
from apps.Nodes.views import main_page, index, node_view, port_view
from apps.Nodes.views import node_list, port_list
from apps.Nodes.views import node_edit, port_edit, node_delete, port_delete
from apps.Nodes.views import NodeList, PortList, NodeCreate, PortCreate
from apps.Nodes.views import NodeUpdate, PortUpdate, NodeDelete, PortDelete
from apps.Nodes.views import NodeAPI, PortAPI

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newNode$', NodeCreate.as_view(), name='newNode'),
	re_path(r'^newPort$', PortCreate.as_view(), name='newPort'),
	re_path(r'^listNode$', NodeList.as_view(), name='listNode'),
	re_path(r'^listPort$', PortList.as_view(), name='listPort'),
	re_path(r'^editNode/(?P<pk>[\w|\W]+)/$', NodeUpdate.as_view(), name='editNode'),
	re_path(r'^editPort/(?P<pk>[\w|\W]+)/$', PortUpdate.as_view(), name='editPort'),
	re_path(r'^deleteNode/(?P<pk>[\w|\W]+)/$', NodeDelete.as_view(), name='deleteNode'),
	re_path(r'^deletePort/(?P<pk>[\w|\W]+)/$', PortDelete.as_view(), name='deletePort'),
	re_path(r'^apiNode$', NodeAPI.as_view(), name='apiNode'),
	re_path(r'^apiPort$', PortAPI.as_view(), name='apiPort'),
]