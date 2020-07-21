import json
import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from listas.forms import SalidaForm
from listas.mixins import ValidatePermissionRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from listas.models import Salida, Producto, DetSalida


class SalidaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Salida
    template_name = 'salida/list.html'
    permission_required = 'view_salida'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Salida.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetSalida.objects.filter(salida_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha Ocurrido Un Error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Salidas'
        context['create_url'] = reverse_lazy('sale_create')
        context['list_url'] = reverse_lazy('sale_list')
        context['entity'] = 'Salidas'
        return context


class SalidaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Salida
    form_class = SalidaForm
    template_name = 'salida/create.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'add_salida'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    salida = Salida()
                    salida.fecha = vents['fecha']
                    salida.responsable_id = vents['responsable']
                    salida.total = float(vents['total'])
                    salida.save()
                    for i in vents['products']:
                        det = DetSalida()
                        det.salida_id = salida.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.save()

                    data={'id':salida.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Salida'
        context['entity'] = 'Salidas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SalidaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Salida
    form_class = SalidaForm
    template_name = 'salida/create.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'change_salida'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    salida = self.get_object()
                    salida.fecha = vents['fecha']
                    salida.responsable_id = vents['responsable']
                    salida.save()
                    salida.detsalida_set.all().delete()
                    for i in vents['products']:
                        det = DetSalida()
                        det.salida_id = salida.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.save()
                    data = {'id': salida.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetSalida.objects.filter(salida_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Salida'
        context['entity'] = 'Salidas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context

class SalidaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Salida
    template_name = 'salida/delete.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'delete_salida'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Salida'
        context['entity'] = 'Salidas'
        context['list_url'] = self.success_url
        return context


class SalidaInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('salida/invoice.html')
            context = {
                'salida': Salida.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Gestion Ing Biomedica', 'ruc': '9999999999999', 'address': 'Medellin, Colombia'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logog.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('sale_list'))