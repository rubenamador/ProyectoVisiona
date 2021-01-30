from django.template import Library
from apps.Links.models import Link

register = Library()

def links_filter(object_list):
	#Recorremos la lista y si el puerto de destino es igual puerto de entrada igualamos el id
	for i in range(0, object_list.count()):
		for j in range(0, object_list.count()):
			if object_list[i].source.id == object_list[j].dest.id:
				object_list[j].id = object_list[i].id
	#Si dos ids son iguales lo borramos
	for i in range(0, object_list.count()):
		if object_list[i].id == object_list[i].dest.id:
			object_list[i].id = " "
			object_list[i].source.id = " "
			object_list[i].dest.id = " "
	
	#	object_list[0].id = "aaa"
	
	return object_list

register.filter("links_filter", links_filter)