from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.Links.forms import LinkForm

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
		return redirect('Links:index')
	else:
		form = LinkForm()
	return render(request, 'links/form.html', {'form':form})
