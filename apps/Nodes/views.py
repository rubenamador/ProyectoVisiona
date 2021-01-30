from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView
import json

from apps.Nodes.forms import NodeForm, PortForm
from apps.Nodes.models import Node, Port
from apps.Nodes.serializers import NodeSerializer, PortSerializer

import pymongo
from pymongo import MongoClient
from json import loads
import fileinput

from urllib.request import urlopen, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, install_opener

# Create your views here.

def main_page(request):
	#return HttpResponse("Pagina Principal Aplicacion Nodes")
	return render(request, 'nodes/index.html')
	
def index(request):
	#return HttpResponse("Indice Aplicacion Nodes")
	return render(request, 'nodes/index.html')

def node_view(request):
	if request.method == 'POST':
		form = NodeForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('Nodes:listNode')
	else:
		form = NodeForm()		
	return render(request, 'nodes/form.html', {'form':form})
	
def port_view(request):
	if request.method == 'POST':
		form = PortForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('Nodes:listPort')
	else:
		form = PortForm()		
	return render(request, 'nodes/form.html', {'form':form})

def node_list(request):
	node = Node.objects.all().order_by('id')
	contexto = {'nodes':node}
	return render(request, 'nodes/node_list.html', contexto)
	
def port_list(request):
	port = Port.objects.all().order_by('id')
	contexto = {'ports':port}
	return render(request, 'nodes/port_list.html', contexto)

def node_edit(request, id_node):
	node = Node.objects.get(id=id_node)
	if request.method == 'GET':
		form = NodeForm(instance=node)
	else:
		form = NodeForm(request.POST, instance=node)
		if form.is_valid():
			form.save()
		return redirect('Nodes:listNode')
	return render(request, 'nodes/form.html', {'form':form})
	
def port_edit(request, id_port):
	port = Port.objects.get(id=id_port)
	if request.method == 'GET':
		form = PortForm(instance=port)
	else:
		form = PortForm(request.POST, instance=port)
		if form.is_valid():
			form.save()
		return redirect('Nodes:listPort')
	return render(request, 'nodes/form.html', {'form':form})

def node_delete(request, id_node):
	node = Node.objects.get(id=id_node)
	if request.method == 'POST':
		node.delete()
		return redirect('Nodes:listNode')
	return render(request, 'nodes/node_delete.html', {'node':node})
	
def port_delete(request, id_port):
	port = Port.objects.get(id=id_port)
	if request.method == 'POST':
		port.delete()
		return redirect('Nodes:listPort')
	return render(request, 'nodes/port_delete.html', {'port':port})

class NodeList(ListView):
	model = Node
	template_name = 'nodes/node_list.html'

class PortList(ListView):
	model = Port
	template_name = 'nodes/port_list.html'

class NodeCreate(CreateView):
	model = Node
	form_class = NodeForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listNode')

class PortCreate(CreateView):
	model = Port
	form_class = PortForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listPort')

class NodeUpdate(UpdateView):
	model = Node
	form_class = NodeForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listNode')
	
class PortUpdate(UpdateView):
	model = Port
	form_class = PortForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listPort')

class NodeDelete(DeleteView):
	model = Node
	template_name = 'nodes/node_delete.html'
	success_url = reverse_lazy('Nodes:listNode')
	
class PortDelete(DeleteView):
	model = Port
	template_name = 'nodes/port_delete.html'
	success_url = reverse_lazy('Nodes:listPort')

class NodeAPI(APIView):
	serializer = NodeSerializer
	
	def get(self, request, format=None):
		lista = Node.objects.all()
		response = self.serializer(lista, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')

class PortAPI(APIView):
	serializer = PortSerializer
	
	def get(self, request, format=None):
		lista = Port.objects.all()
		response = self.serializer(lista, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')

class NodeInfo(ListView):
	model = Node
	template_name = 'nodes/node_info.html'
	
	def get_context_data(self, **kwargs):
		context = super(NodeInfo, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		node = self.model.objects.get(id=pk)
		context['node'] = node
		#ports = Port.objects.all()
		ports_of_node = query_get_ports_by_node(str(node))
		ports = []
		for i in range(len(ports_of_node)):
			ports.append(ports_of_node[i]["_id"])
		context['ports'] = ports
		#links = Links.objects.all()
		#links_of_node = query_get_ports_by_node(str(node))
		#context['links'] = links_of_node
		return context

def all_nodes_delete(request):
	if request.method == 'POST':
		Node.objects.all().delete()
		return redirect('Nodes:listNode')
	return render(request, 'nodes/all_nodes_delete.html')

def all_ports_delete(request):
	if request.method == 'POST':
		Port.objects.all().delete()
		return redirect('Nodes:listPort')
	return render(request, 'nodes/all_ports_delete.html')

def import_all(request):
	if request.method == 'POST':
		mongoimport_all()
		return redirect('Nodes:listNode')
	return render(request, 'nodes/import_all.html')

def get_topology(request):
	if request.method == 'POST':
		get_json_from_url()
		return redirect('Nodes:listNode')
	return render(request, 'nodes/get_topology.html')

########### NO SON VISTAS

def query_get_ports_by_node(node):
	client = MongoClient('localhost', 27017)
	db = client.djongo
	Nodes_port = db.Nodes_port
	
	pipeline = [{"$match":{"node_id":node}},  
				{"$group": {"_id": "$id"}}]
	return list(db.Nodes_port.aggregate(pipeline))

def mongoimport_all():
	mongoimport_all_nodes()
	mongoimport_all_ports()
	mongoimport_all_links()

def mongoimport_all_nodes():
	#query_get_all_nodes_info()
	mongoimport('localhost', 27017, 'djongo', 'Nodes_node', 'node.json')

def mongoimport_all_ports():
	#query_get_all_ports_info()
	mongoimport('localhost', 27017, 'djongo', 'Nodes_port', 'port.json')

def mongoimport_all_links():
	#query_get_all_links_info()
	mongoimport('localhost', 27017, 'djongo', 'Links_link', 'link.json')
	
#def query_get_and_import_all():
#	query_get_and_import_all_nodes()
#	query_get_and_import_all_ports()
#	query_get_and_import_all_links()

#def query_get_and_import_all_nodes():
#	query_get_all_nodes_info()
#	mongoimport('localhost', 27017, 'djongo', 'Nodes_node', 'node.json')

#def query_get_and_import_all_ports():
#	query_get_all_ports_info()
#	mongoimport('localhost', 27017, 'djongo', 'Nodes_port', 'port.json')

#def query_get_and_import_all_links():
#	query_get_all_links_info()
#	mongoimport('localhost', 27017, 'djongo', 'Links_link', 'link.json')

def query_get_all_nodes_info():
	client = MongoClient('localhost', 27017)
	db = client.nets
	nodes = db.nodes
	
	pipeline = [{"$unwind":"$network-topology.topology"},
				{"$unwind":"$network-topology.topology.node"},
				{"$group": {"_id": "$network-topology.topology.node.node-id"}}]
	#pprint.pprint(list(db.nodes.aggregate(pipeline)))
	
	content = list(db.nodes.aggregate(pipeline))
	#data = content.decode("utf-8")
	
	filename = 'node.json'
	with open(filename, 'w') as outfile:
		json.dump(content, outfile)
	
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			print(line.replace("_id", "id").replace("},", "},\n"), end='')
	
	i = 0
	number = '00'
	name = ""
	catch = False
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			if(line[9:17] == "openflow"):
				if(line[19] is '\"'):
					number = line[18]
				else:
					number = line[18:20]
				name = "openflow:" + number
			
			if(line[9:13] == "host"):
				name = line[9:31]
			
			print(line.replace("}", ", \"name\":\"" + name + "\"}"), end='')
			i = i + 1

def query_get_all_ports_info():
	client = MongoClient('localhost', 27017)
	db = client.nets
	nodes = db.nodes
	
	pipeline = [{"$unwind":"$network-topology.topology"},
				{"$unwind":"$network-topology.topology.node"},
				{"$unwind":"$network-topology.topology.node.termination-point"},
				{"$group": {"_id": "$network-topology.topology.node.termination-point.tp-id"}}]
	#pprint.pprint(list(db.nodes.aggregate(pipeline)))
	
	content = list(db.nodes.aggregate(pipeline))
	#data = content.decode("utf-8")
	
	filename = 'port.json'
	with open(filename, 'w') as outfile:
		json.dump(content, outfile)

	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			print(line.replace("_id", "id").replace("},", "},\n"), end='')

	number = '00'
	name = ""
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			if(line[9:17] == "openflow"):
				if(line[19] is ':'):
					number = line[18]
				else:
					number = line[18:20]
				name = "openflow:" + number
			
			if(line[9:13] == "host"):
				name = line[9:31]
			print(line.replace("}", ", \"node_id\":\"" + name + "\"}"), end='')

def query_get_all_links_info():
	client = MongoClient('localhost', 27017)
	db = client.nets
	nodes = db.nodes
	
	pipeline = [{"$unwind":"$network-topology.topology"},
				{"$unwind":"$network-topology.topology.link"},
				{"$group": {"_id": "$network-topology.topology.link"}}]
	#pprint.pprint(list(db.nodes.aggregate(pipeline)))
	
	content = list(db.nodes.aggregate(pipeline))
	#data = content.decode("utf-8")
	
	filename = 'link.json'
	with open(filename, 'w') as outfile:
		json.dump(content, outfile)
	
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			print(line.replace("_id\": {\"link-id", "id").replace("\"source\": {", "").replace("\"destination\": {", "")
			.replace("source-tp", "source_id").replace("dest-tp", "dest_id")
			.replace("source-node", "source_node_id").replace("dest-node", "dest_node_id")
			.replace("},", ",").replace("}},", "},").replace("}}}]", "}]"), end='')
			
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			print(line.replace("},", "},\n"), end='')
	
	base = ""
	sustituto = ""
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			encontradoBase = False
			encontradoSustituto = False
			for i in range(len(line)):
				if(line[i] == '/' and encontradoSustituto == False):
					sustituto = line[0:i]
					encontradoSustituto = True
				if(line[i:i+12] == "dest_node_id" and encontradoBase == False):
					total = i-4
					base = line[0:total]
					encontradoBase = True
			
			if(encontradoSustituto == True and encontradoBase == True):
				print(line.replace(base, sustituto), end='')
			else:
				print(line, end='')

			

def mongoimport(host, port, db, collection, file):
	client = MongoClient(host, port)
	db = client[db]
	collection_currency = db[collection]
	
	with open(file) as f:
		file_data = json.load(f)
	
	collection_currency.insert(file_data)
	client.close()
	
def get_json_from_url():
	url = 'http://192.168.38.128:8181/restconf/operational/network-topology:network-topology/'
	username = 'admin'
	password = 'admin'
	p = HTTPPasswordMgrWithDefaultRealm()
	
	p.add_password(None, url, username, password)
	
	handler = HTTPBasicAuthHandler(p)
	opener = build_opener(handler)
	install_opener(opener)
	
	content = urlopen(url).read()
	#print(content)
	
	data = content.decode("utf-8")
	print(data)
	
	filename = 'data.json'
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)
	
	with fileinput.FileInput(filename, inplace=True) as file:
		for line in file:
			print(line.replace("\\", "").replace("\"{", "{").replace("}\"", "}"), end='')
	
	client = MongoClient('localhost', 27017)
	db = client.nets
	db.nodes.remove({})
	mongoimport('localhost', 27017, 'nets', 'nodes', 'data.json')
	
	query_get_all_nodes_info()
	query_get_all_ports_info()
	query_get_all_links_info()
