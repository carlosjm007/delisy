from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from principal.models import *
# Register your models here.

@admin.register(Pais)
class PaisAdmin(ImportExportActionModelAdmin):
	pass

@admin.register(Ciudad)
class CiudadAdmin(ImportExportActionModelAdmin):
	pass

@admin.register(Url)
class UrlAdmin(ImportExportActionModelAdmin):
	pass

@admin.register(Tienda)
class TiendaAdmin(ImportExportActionModelAdmin):
	pass