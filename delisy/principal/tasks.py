from background_task import background
from principal.models import *
import sys, requests, json, time
from django.conf import settings

class scraping_uber(object):
	csrftoken = ""
	ciudad = ""
	client = ""
	def __init__(self, ciudad):
		self.ciudad = ciudad
		self.client = requests.session()
		Tienda.objects.filter(ciudad = self.ciudad).update(disponible = False)

	def peticion_csrftoken(self):
		bandera = True
		page = self.client.get(self.ciudad.url_pagina)
		pagina = str(page.content)
		ubicacion_csrf = pagina.find("window.csrfToken")
		while(bandera):
			self.csrftoken = self.csrftoken + pagina[ubicacion_csrf]
			ubicacion_csrf = ubicacion_csrf + 1
			if pagina[ubicacion_csrf] == ";":
				bandera = False
		self.csrftoken = self.csrftoken.replace("window.csrfToken","").replace(" = ","").replace("\\'","")

	def peticion_tiendas(self):
		headers={
			"Referer":self.ciudad.url_pagina,
			"x-csrf-token":self.csrftoken,
			"content-type": "application/json",
			"x-requested-with": "XMLHttpRequest"}
		for u in Url.objects.filter(ciudad = self.ciudad):
			r = self.client.post(u.url, headers=headers, json=json.loads(u.request_payload))
			data = r.json()
			'''
			if u.primera:
				for ind, i in enumerate(data["marketplace"]["feed"]["feedItems"]):
					if "storePayload" in i["payload"]:
						p = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"]
			else:
				for ind, i in enumerate(data["feed"]["feedItems"]):
					if "storePayload" in i["payload"]:
						p = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"]
			'''
			if u.primera:
				datos = data["marketplace"]["feed"]["feedItems"]
			else:
				datos = data["feed"]["feedItems"]
			for ind, i in enumerate(datos):
				if "storePayload" in i["payload"]:
					tienda_nombre = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"]
					tienda_nombre = tienda_nombre.replace(" ","+")
					tienda_nombre = tienda_nombre.replace("&","and")
					tiendita = Tienda.objects.filter(uuid = i["uuid"])
					if str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]).find("Min") > 0:
						a = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-36.88824,174.764533&radius=5000&type=restaurant&keyword='+ tienda_nombre +'&key=AIzaSyCDvjQYoCmk6_DJSF7liYmoPF9I3MClEPY')
						for t in a.json()["results"]:
							latitud = t['geometry']['location']["lat"]
							longitud = t['geometry']['location']["lng"]
							calificacion = t['rating']
					else:
						latitud = 0.0
						longitud = 0.0
						calificacion = 0.0
					if len(tiendita) == 0:
						Tienda.objects.create(
							nombre = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"],
							uuid = i["uuid"],
							ciudad = self.ciudad,
							latitud = latitud,
							longitud = longitud,
							calificacion = calificacion,
							disponible = str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]).find("Min") > 0
							)
					else:
						Tienda.objects.filter(uuid = i["uuid"]).update(
							nombre = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"],
							disponible = str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]).find("Min") > 0,
							ciudad = self.ciudad,
							latitud = latitud,
							longitud = longitud,
							calificacion = calificacion
							)
					print(tienda_nombre, str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]).find("Min") > 0, str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]))
					time.sleep(1)
					#p = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"]

			######
			### Y aquí recorre todos los restaurantes


#@background(schedule=30)
def obtener_tiendas():
	city = Ciudad.objects.all().first()
	prueba = scraping_uber(ciudad = city)
	prueba.peticion_csrftoken()
	prueba.peticion_tiendas()
	el_json = []
	tienditas = Tienda.objects.filter(disponible = True)
	for ti in tienditas:
		el_json.append({
			"lat":str(ti.latitud),
			"lng":str(ti.longitud),
			"calificacion":str(ti.calificacion)
			})
	with open('%s/jsons/%s.json'%(settings.STATIC_ROOT,city.id), 'w') as f:
		json.dump(el_json, f)
	#########################
	#### Aquí es donde comienza el scraping
	#########################
