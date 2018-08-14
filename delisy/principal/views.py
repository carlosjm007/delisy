from django.shortcuts import render
from principal.models import *

# Create your views here.
def index(request):
    # View code here...
    return render(
    	request,
    	'principal/index.html',
    	{
    		"ciudad_inicio":Ciudad.objects.all().first(),
    		"ciudades":Ciudad.objects.all()
    	}
    )