from django.shortcuts import render,redirect
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def crear_promocion(request):
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = PromocionForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                # Guarda el libro en la base de datos
                formulario.save()
                return redirect("index")
            except Exception as error:
                print(error)
    
    return render(request, 'examen/promocion/crear_promocion.html', {'formulario': formulario}) 

def lista_promociones(request):
    # Recuperar todos las promociones desde la base de datos
    promociones = Promocion.objects.all()

    # Pasar la lista de promociones a la plantilla
    return render(request, 'examen/lista_promociones.html', {
        'promociones': promociones
    })


class BusquedaPromocionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
def promocion_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            QSpromociones = Promocion.objects.all()
            
            # Obtenemos los filtros del formulario
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha_fin_desde = formulario.cleaned_data.get('fecha_fin_desde')
            fecha_fin_hasta = formulario.cleaned_data.get('fecha_fin_hasta')
            promocion_minima = formulario.cleaned_data.get('promocion_minima')
            usuarios = formulario.cleaned_data.get('usuarios')
            estado = formulario.cleaned_data.get('estado')
            
            if textoBusqueda:
                QSpromociones = QSpromociones.filter(
                    Q(nombre__icontains=textoBusqueda) | Q(descripcion__icontains=textoBusqueda)
                )
                mensaje_busqueda += f" Nombre que contenga la palabra '{textoBusqueda}'\n"
            
            if fecha_fin_desde:
                QSpromociones = QSpromociones.filter(fecha_fin__gte=fecha_fin_desde)
                mensaje_busqueda += f" Fecha de ingreso desde: {fecha_fin_desde.strftime('%d-%m-%Y')}\n"
            
            if fecha_fin_hasta:
                QSpromociones = QSpromociones.filter(fecha_fin__lte=fecha_fin_hasta)
                mensaje_busqueda += f" Fecha de ingreso hasta: {fecha_fin_hasta.strftime('%d-%m-%Y')}\n"
            
            if promocion_minima is not None:
                QSpromociones = QSpromociones.filter(descuento__gte=promocion_minima)
                mensaje_busqueda += f" Puntos mínimos: {promocion_minima}\n"
            
            if usuarios:
                  # Extraer los usuarios de las promociones (solo el campo 'nombre' de cada objeto usuarios)
                nombres_usuario = usuarios.values_list('nombre', flat=True)
                 # Filtrar QSpromociones por los nombres de los usuarios
                QSpromociones = QSpromociones.filter(usuarios__nombre__in=nombres_usuario)
                mensaje_busqueda += f" Buscado por usuarios: {', '.join(nombres_usuario)}\n"
            
            if estado:
                QSpromociones = QSpromociones.filter(esta_activa=True)
                mensaje_busqueda += " Estado: Activo\n"
            
            promociones = QSpromociones.all()
    
            return render(request, 'examen/promocion/buscar_promocion.html', {
                "promociones_mostrar": promociones,
                "texto_busqueda": mensaje_busqueda
            })
    else:
        formulario = BusquedaAvanzadaPromocionForm(None)
    
    return render(request, 'examen/promocion/busqueda_avanzada.html', {"formulario": formulario})




def promocion_editar(request, promocion_id):
 
    promocion = Promocion.objects.get(id=promocion_id)  
    
    datosFormulario = None  # Inicializamos la variable para los datos del formulario

    if request.method == "POST":
        datosFormulario = request.POST  # Capturamos los datos enviados por el formulario
    
 
    formulario = PromocionForm(datosFormulario, instance=promocion)
    
    if request.method == "POST":
        if formulario.is_valid():  # Validamos el formulario
            try:
                # Guardamos los cambios en la base de datos
                formulario.save()
                # Mostramos un mensaje de éxito
                messages.success(
                    request,
                    f"Se ha editado la promocion de '{formulario.cleaned_data.get('nombre')}' correctamente."
                )
                return redirect('lista_promociones')  
            except Exception as error:
                print(error)  
    
 
    return render(
        request,
        'examen/promocion/crear_promocion.html', 
        {"formulario": formulario, "promocion": promocion}
    )
    
    
def promocion_eliminar(request, promocion_id):
    try:
        promcion = Promocion.objects.get(id=promocion_id)
        

        promcion.delete()
        

        messages.success(request, f"Se ha eliminado la promocion  {promcion.nombre} correctamente.")
        
    except Promocion.DoesNotExist:
  
        messages.error(request, "La promocion no existe.")
    except Exception as error:
        print(error)
    

    return redirect('lista_promociones')  