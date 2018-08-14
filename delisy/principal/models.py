from django.db import models
from decimal import Decimal
# Create your models here.

class Pais(models.Model):
	nombre = models.CharField(max_length=255)
	def __str__(self):
		return "%s" %(self.nombre)
	class Meta:
		verbose_name = "Pais"
		verbose_name_plural = "Paises"

class Ciudad(models.Model):
	nombre = models.CharField(max_length=255)
	latitud = models.FloatField()
	longitud = models.FloatField()
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
	url_pagina = models.URLField()
	def __str__(self):
		return "%s" %(self.nombre)
	class Meta:
		verbose_name = "Ciudad"
		verbose_name_plural = "Ciudades"

class Url(models.Model):
	ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
	url = models.URLField()
	primera = models.BooleanField(default=False)
	offset = models.CharField(max_length=15, null=True, blank=True)
	pageSize = models.CharField(max_length=15, null=True, blank=True)
	request_payload = models.CharField(max_length=1000)
	def __str__(self):
		return "%s" %(self.ciudad.nombre)
	class Meta:
		verbose_name = "URL"
		verbose_name_plural = "URLs"

class Tienda(models.Model):
	nombre = models.CharField(max_length=255)
	uuid = models.CharField(max_length=50)
	latitud = models.FloatField(default=0.0)
	longitud = models.FloatField(default=0.0)
	ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
	calificacion = models.DecimalField(default=Decimal('0.0'), max_digits=3, decimal_places=1)
	disponible = models.BooleanField(default=True)
	def __str__(self):
		return "%s - %s" %(self.nombre, self.ciudad.nombre)
	class Meta:
		verbose_name = "Tienda"
		verbose_name_plural = "Tiendas"
