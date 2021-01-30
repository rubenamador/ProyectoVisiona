from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.Nodes.forms import NodeForm, PortForm
from apps.Nodes.models import Node, Port

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