from django.urls import re_path
from apps.Nodes.views import main_page, index, node_view, port_view

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
	re_path(r'^newNode$', node_view, name='newNode'),
	re_path(r'^newPort$', port_view, name='newPort'),
]