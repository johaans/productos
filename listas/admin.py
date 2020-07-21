from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django import forms
from .models import Salida,Producto,DetSalida
# Register your models here.

class Detsalidaresource(resources.ModelResource):
    class Meta:
        model = DetSalida

class Detsalidaadmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('salida', 'prod','cant')
    list_filter = ['salida', 'prod','cant']
    search_fields = ('salida', 'prod','cant')
    resource_class=Detsalidaresource
admin.site.register(DetSalida,Detsalidaadmin)

class Productoresource(resources.ModelResource):
    class Meta:
        model = Producto


class Productoadmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('nombre', 'descripcion','categoria')
    list_filter = ['nombre', 'descripcion','categoria']
    search_fields = ('nombre', 'descripcion','categoria','autor')
    resource_class=Productoresource
admin.site.register(Producto,Productoadmin)


class Salidaresource(resources.ModelResource):
    class Meta:
        model = Salida

class Salidaadmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('responsable','fecha')
    list_filter = ['responsable','fecha']
    search_fields = ('responsable','fecha')
    resource_class=Salidaresource
admin.site.register(Salida,Salidaadmin)
