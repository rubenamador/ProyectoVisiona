from django.template import Library
from apps.Links.models import Link

register = Library()

def snodes_filter(object_list):
	#Recorremos la lista y si el nodo de partida ya ha sido visto lo eliminamos
	for i in range(0, object_list.count()):
		for j in range(i + 1, object_list.count()):
			if object_list[i].source.node.id == object_list[j].source.node.id:
				object_list[j].id = " "
				object_list[j].source.id = " "
				object_list[j].dest.id = " "
	
	return object_list

register.filter("snodes_filter", snodes_filter)