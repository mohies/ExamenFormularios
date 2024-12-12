from django import forms  # Importa el módulo de formularios
from django.forms import ModelForm  # Importa ModelForm directamente
from .models import *
from datetime import datetime, date, timedelta
from django.forms import DateInput
import datetime


class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'producto', 'usuarios', 'fecha_inicio', 'fecha_fin', 'descuento', 'esta_activa']
        widgets = { 
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la promoción'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'usuarios': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'esta_activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': "Nombre de la promoción",
            'descripcion': "Descripción de la promoción",
            'producto': "Producto de la promoción",
            'usuarios': "Usuarios de la promoción",
            'fecha_inicio': "Fecha inicio",
            'fecha_fin': "Fecha fin",
            'descuento': "Descuento",
            'esta_activa': "¿Tiene promoción?",
        }
        help_texts = {
            'nombre': "Debe ser un nombre único.",
            'descripcion': "La descripción debe tener al menos 100 caracteres.",
            'producto': "Seleccione un producto que pueda tener promociones.",
            'usuarios': "Seleccione usuarios que sean mayores de edad.",
            'fecha_inicio': "La fecha de inicio debe ser anterior a la fecha de fin.",
            'fecha_fin': "La fecha de fin no puede ser anterior a la fecha actual.",
            'descuento': "El descuento debe ser un valor entre 0 y 10.",
        }

    def clean(self):
        super().clean()

        # Obtener los campos
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        producto = self.cleaned_data.get('producto')
        usuarios = self.cleaned_data.get('usuarios')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        descuento = self.cleaned_data.get('descuento')

        #  Validaciones
        if Promocion.objects.filter(nombre=nombre).exists():
            self.add_error('nombre', 'Ya existe una promoción con ese nombre.')

        if descripcion and len(descripcion) < 100:
            self.add_error('descripcion', 'La descripción debe tener al menos 100 caracteres.')

        if producto and not producto.puede_tener_promociones:
            self.add_error('producto', 'El producto seleccionado no permite tener promociones.')

        if usuarios:
            for usuario in usuarios: #recorremos los usuarios porque debe tener varios usuarios
                if usuario.edad < 18:
                    self.add_error('usuarios', f'El usuario {usuario.nombre} debe ser mayor de edad.')

        if fecha_inicio and fecha_fin and fecha_inicio >= fecha_fin:
            self.add_error('fecha_inicio', 'La fecha de inicio debe ser anterior a la fecha de fin.')
    
        if fecha_fin and fecha_fin < date.today():
            self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha actual.')

        if descuento is not None and (descuento < 0 or descuento > 10):
            self.add_error('descuento', 'El descuento debe ser un valor entre 0 y 10.')

        return self.cleaned_data
    
    
class BusquedaAvanzadaPromocionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o Descripcion'}), label="Nombre o Descripcion")

    fecha_fin_desde = forms.DateField(label="Fecha Desde", 
                                  required=False, 
                                  widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    fecha_fin_hasta = forms.DateField(label="Fecha Hasta", 
                                  required=False,
                                  widget=forms.DateInput(format="%Y-%m-%d", 
                                                         attrs={"type": "date", "class": "form-control"}))
    promocion_minima = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Promocion minima"
    )
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),  # obtener todos los usuarios de la base de datos
        widget=forms.SelectMultiple(),  # Usas el widget de casillas múltiples
        required=False,  
        help_text="Selecciona los usuarios"  
    )
    
    estado = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )
    
    
    def clean(self):
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_fin_desde = self.cleaned_data.get('fecha_fin_desde')
        fecha_fin_hasta = self.cleaned_data.get('fecha_fin_hasta')
        promocion_minima=self.cleaned_data.get('promocion_minima')
        usuarios=self.cleaned_data.get('usuarios')
        estado=self.cleaned_data.get('estado')
        
        if not (textoBusqueda or fecha_fin_desde or fecha_fin_hasta or promocion_minima or usuarios or estado):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_fin_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_fin_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('promocion_minima', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('usuarios', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('estado', 'Debe introducir al menos un valor en un campo del formulario')
            
        if fecha_fin_desde and fecha_fin_hasta and fecha_fin_hasta < fecha_fin_desde:
            self.add_error('fecha_fin_hasta', 'La fecha "hasta" no puede ser anterior a la fecha "desde"')
        
        if promocion_minima is not None and (promocion_minima < 0 or promocion_minima>10):
            self.add_error('promocion_minima', 'La promocion debe ser un valor positivo.')  
            
        return self.cleaned_data  
    
    
    
        

