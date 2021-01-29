from django.urls import re_path
from apps.Links.views import main_page, index

urlpatterns = [
	re_path(r'^$', main_page),
	re_path(r'^index$', index, name='index'),
]