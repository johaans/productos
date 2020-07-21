from django import forms
from .models import *



class BodegasForm(forms.ModelForm):
    """Form definition for Categoria."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']='form-control'
            form.field.widget.attrs['autocomplete']='off'
            self.fields['nombre'].widget.attrs['autofocus']='True'
        

    class Meta:
        """Meta definition for Categoriaform."""

        model = Producto
        fields = ('__all__')

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']='form-control'
            form.field.widget.attrs['autocomplete']='off'
            self.fields['nombre'].widget.attrs['autofocus']='True'

    class Meta:
        model = Producto
        fields = '__all__'
        exclude=['user_updated','user_creation']
        

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']='form-control'
            form.field.widget.attrs['autocomplete']='off'
            self.fields['nombre'].widget.attrs['autofocus']='True'

    class Meta:
        model = Producto
        fields = '__all__'
        exclude=['user_updated','user_creation']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }


class SalidaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Salida
        fields = '__all__'
        widgets = {
            'responsable': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }