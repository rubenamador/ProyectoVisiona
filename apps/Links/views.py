from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.Links.forms import LinkForm
from apps.Links.models import Link

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
	success_url = reverse_lazy('Links:listLink')

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