from background_task import background
from principal.models import *

@background(schedule=3600)
def obtener_tiendas():
	Tienda.objects.all().delete()
	#########################
	#### Aquí es donde comienza el scraping
	#########################
