from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def main_page(request):
	return HttpResponse("Pagina Principal Aplicacion Nodes")
	
def index(request):
	return HttpResponse("Indice Aplicacion Nodes")
