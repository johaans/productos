from django.db import models
from django.utils import timezone
from datetime import datetime
from random import randint
from django.conf import settings
from django.urls import reverse
from django.forms.models import model_to_dict
from .choices import seleccion_cat
from inventario.settings import MEDIA_URL, STATIC_URL
from inventario.basemodel.models import BaseModel
from crum import get_current_user


class Producto(BaseModel):
    codigo = models.IntegerField(default=0,unique=True)
    nombre = models.CharField('NOMBRE', max_length=100)
    categoria=models.CharField('Categoria',choices=seleccion_cat,max_length=18)
    descripcion=models.TextField('DESCRIPCION',max_length=2000,null=True,blank=True)
    stockinicial = models.IntegerField(default=0)
    entradas = models.IntegerField(default=0)
    salidas = models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    final = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='producto/%Y/%m', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['imagen'] = self.get_image()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Producto, self).save()


    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Salida(models.Model):
    """Model definition for Salidas."""
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL,default=settings.AUTH_USER_MODEL, max_length=400, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.now)
    total=models.IntegerField(default=0)



    class Meta:
        """Meta definition for Salida."""

        verbose_name = 'Salidas'
        verbose_name_plural = 'Salidas'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Salidas."""
        return self.responsable.get_username()

    def toJSON(self):
        item = model_to_dict(self)
        item['responsable'] =self.responsable.get_username()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsalida_set.all()]
        return item



class DetSalida(models.Model):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['salida'])
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Salida'
        verbose_name_plural = 'Detalle de Salidas'
        ordering = ['id']