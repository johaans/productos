from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from listas.vistas.product.views import *
from listas.vistas.salida.views import *

urlpatterns = [
    path('lista/repuestos/',ProductoListView.as_view(), name='lista_repuestos'),
    path('lista/repuestos2/',ProductoListView.as_view(), name='lista_categorias'),
    path('lista/crear/',ProductoCreateView.as_view(), name='crear_bodega'),
    path('lista/editar/<int:pk>/',ProductoUpdateView.as_view(), name='editar_bodega'),
    path('lista/borrar/<int:pk>/',ProductoDeleteView.as_view(), name='borrar_categoria'),
    #path('categorias/form/', CategoryFormView.as_view(), name='category_form'),
    # home
    #path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # product
    path('product/list/', ProductoListView.as_view(), name='product_list'),
    path('product/add/', ProductoCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductoUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductoDeleteView.as_view(), name='product_delete'),
    # salida
    path('salida/list/', SalidaListView.as_view(), name='sale_list'),
    path('salida/add/', SalidaCreateView.as_view(), name='sale_create'),
    path('salida/delete/<int:pk>/', SalidaDeleteView.as_view(), name='sale_delete'),
    path('salida/update/<int:pk>/', SalidaUpdateView.as_view(), name='sale_update'),
    path('salida/invoice/pdf/<int:pk>/', SalidaInvoicePdfView.as_view(), name='sale_invoice_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

