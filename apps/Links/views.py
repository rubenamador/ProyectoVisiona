from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from rest_framework.views import APIView
import json

from apps.Links.forms import LinkForm
from apps.Links.models import Link
from apps.Links.serializers import LinkSerializer

from apps.Nodes.models import Node, Port
from apps.Nodes.forms import PortNodeForm, PortForm

import simplejson as json
from django.core import serializers

import pymongo
from pymongo import MongoClient
from json import loads
import fileinput

# Create your views here.

def main_page(request):
	#return HttpResponse("Pagina Principal Aplicacion Links")
	return render(request, 'links/index.html')
	
def index(request):
	#return HttpResponse("Indice Aplicacion Links")
	return render(request, 'links/index.html')

def link_view(request):
	if request.method == 'POST':
		form = LinkForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('Links:listLink')
	else:
		form = LinkForm()
	return render(request, 'links/form.html', {'form':form})

def link_list(request):
	link = Link.objects.all().order_by('id')
	contexto = {'links':link}
	return render(request, 'links/link_list.html', contexto)

def link_edit(request, id_link):
	link = Link.objects.get(id=id_link)
	if request.method == 'GET':
		form = LinkForm(instance=link)
	else:
		form = LinkForm(request.POST, instance=link)
		if form.is_valid():
			form.save()
		return redirect('Links:listLink')
	return render(request, 'links/form.html', {'form':form})

def link_delete(request, id_link):
	link = Link.objects.get(id=id_link)
	if request.method == 'POST':
		link.delete()
		return redirect('Links:listLink')
	return render(request, 'links/link_delete.html', {'link':link})

class LinkList(ListView):
	model = Link
	template_name = 'links/link_list.html'

class LinkCreate(CreateView):
	model = Link
	form_class = LinkForm
	template_name = 'links/form.html'
	success_url = reverse_lazy('Links:updateAllLinks')

class LinkUpdate(UpdateView):
	model = Link
	form_class = LinkForm
	template_name = 'links/form.html'
	success_url = reverse_lazy('Links:listLink')

class LinkDelete(DeleteView):
	model = Link
	template_name = 'links/link_delete.html'
	success_url = reverse_lazy('Links:listLink')

class LinkGraph(ListView):
	model = Link
	template_name = 'links/link_graph.html'

class LinkAPI(APIView):
	serializer = LinkSerializer
	
	def get(self, request, format=None):
		lista = Link.objects.all()
		response = self.serializer(lista, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')

class LinkConnect(FormView):
	model = Node
	form_class = PortNodeForm
	template_name = 'links/link_connect_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(LinkConnect, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		source = self.model.objects.get(id=pk)
		context['source'] = source
		context['nodes'] = Node.objects.all()
		return context

class LinkPath(ListView):
	model = Node
	second_model = Node
	template_name = 'links/link_path.html'
	
	def get_context_data(self, **kwargs):
		context = super(LinkPath, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		pk2 = self.kwargs.get('pk2', 0)
		source = self.model.objects.get(id=pk)
		dest = self.second_model.objects.get(id=pk2)
		context['source'] = source
		context['dest'] = dest
		context['nodes'] = Node.objects.all()
		context['links'] = Link.objects.all()
		cola = []
		path = []
		links = query_get_all_links_info()
		search_path(str(source), str(dest), links, cola, path, str(source))
		#path = path.sort(reverse = True)
		tmp = []
		for i in range(len(path)):
			tmp.append(path[len(path) - (i + 1)])
		path = tmp
		for i in range(len(path)):
			print(str(i) + ". " + path[i])
		context['path'] = path
		send_packet(path, links, "info")
		return context

def all_links_delete(request):
	if request.method == 'POST':
		Link.objects.all().delete()
		return redirect('Links:listLink')
	return render(request, 'links/all_links_delete.html')

def all_links_update(request):
	if request.method == 'POST':
		links = Link.objects.all()
		#Rellenamos los campos de cada link: nodo origen y nodo destino
		for link in links:
			link.source_node = link.source.node
			link.dest_node = link.dest.node
			link.save()
		#Comprobamos que todos los links tienen su duplicado con origen y destino al reves
		for link1 in links:
			exist = False
			for link2 in links:
				if str(link1.dest) == str(link2.id):
					exist = True
			#Si el link no tiene su duplicado, lo creamos
			if exist == False:
				Link.objects.create_link(link1.dest, link1.dest, link1.source, link1.dest_node, link1.source_node)
		return redirect('Links:listLink')
	return render(request, 'links/all_links_update.html')

#### NO SON VISTAS



def query_get_all_links_info():
	client = MongoClient('localhost', 27017)
	db = client.djongo
	Links_link = db.Links_link
	
	#pprint.pprint(list(db.nodes.aggregate(pipeline)))
	
	content = list(db.Links_link.find())
	#data = content.decode("utf-8")
	
	return content

def query_get_number_of_links():
	client = MongoClient('localhost', 27017)
	db = client.djongo
	Links_link = db.Links_link
	
	pipeline = [{"$group": {"_id": "$id"}}, 
				{"$count":"number_of_links"}]
	#pprint.pprint(list(db.nodes.aggregate(pipeline)))
	return list(db.Links_link.aggregate(pipeline))
	
def get_source_node(port):
	client = MongoClient('localhost', 27017)
	db = client.djongo
	Nodes_port = db.Nodes_port
	
	pipeline = [{"$match":{"id":port}},
				{"$group": {"_id": "$node"}}]
	#pprint.pprint(list(db.nodes.aggregate(pipeline)))
	return list(db.Nodes_port.aggregate(pipeline))
	

def get_linked_nodes(nodo):
	nodosConectados = []
	links = query_get_all_links_info()
	list = query_get_number_of_links()

	size = list[0]["number_of_links"]
	print("Size: " + str(size))
	
	for i in range(len(links)):
		#print(links[i]["_id"]["source"]["source-node"])
		source = links[i]["source_node_id"]
		
		
		if (source == nodo):
			dest = links[i]["dest_node_id"]
			nodosConectados.append(dest)
	
	#print(nodosConectados)
	return nodosConectados
	
def search_path(source, dest, links, cola, path, firstSource):
	#print(source)
	#print(cola)
	#stop = input("Pulsa cualquier tecla y despues intro...")
	
	if (len(cola) > 0):
		del cola[0]
		
	#Mirar nodos conectados al nodo dado
	nodosConectados = get_linked_nodes(source)
	terminado = False
	for i in range(len(nodosConectados)):
		#Si un nodo es igual al nodo destino terminar
		if (nodosConectados[i] == dest):
			#print(dest)
			path.append(dest)
			
			if (source != firstSource):
				#del cola
				cola.clear()
				search_path(firstSource, source, links, cola, path, firstSource)
			else:
				path.append(firstSource)
				#for i in range(len(path)):
				#	print(str(i) + ". " + path[i])
					
			terminado = True
		else:
			#Guardar en una cola los nodos conectados
			insert = True
			for j in range(len(cola)):
				if (cola[j] == nodosConectados[i]):
					insert = False
			
			if (insert):
				cola.append(nodosConectados[i])
			
	if (terminado == False):
		search_path(cola[0], dest, links, cola, path, firstSource)

def remove_link(host, port, db, collection, link):
	client = MongoClient(host, port)
	db = client[db]
	collection_currency = db[collection]
	
	collection_currency.remove({"id": link})
	collection_currency.remove({"dest_id": link})
	client.close()
	
def send_packet(path, links, packet):
	
	#Buscamos puerto del nodo origen
	source_port = ""
	for i in range(len(links)):
		if (links[i]["source_node_id"] == path[0] and links[i]["dest_node_id"] == path[1]):
			source_port = links[i]["source_id"]
	
	#Metemos paquete en nodo origen
	print("Enviamos paquete a tabla 0 del nodo " + path[0] + " por cualquier puerto. Ej. " + source_port + "\n") 
	#peticionPOST(links[j]["dest_node_id"], links[j]["dest_id"], paquete) #PeticionPOST(nodo, puerto, paquete)
	
	#Buscamos el puerto por donde enviar paquete al nodo destino
	for i in range(len(path) - 1):
		for j in range(len(links)):
			if (links[j]["source_node_id"] == path[i] and links[j]["dest_node_id"] == path[i+1]):
				print("Obtenemos paquete en tabla 0 del nodo " + links[j]["source_node_id"] + " por puerto " + links[j]["source_id"])
				#paquete = peticionGET(links[j]["source_node_id"], links[j]["source_id"]) #PeticionGET(nodo, puerto)
				print("Enviamos paquete a tabla 0 del nodo " + links[j]["dest_node_id"] + " por puerto " + links[j]["dest_id"] + "\n") 
				#peticionPOST(links[j]["dest_node_id"], links[j]["dest_id"], paquete) #PeticionPOST(nodo, puerto, paquete)
				#paquete = peticionGET(links[j]["source_node_id"], links[j]["source_id"]) #PeticionGET(nodo, puerto)