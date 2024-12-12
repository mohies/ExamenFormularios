from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('crear-promocion/', views.crear_promocion, name='crear_promocion'),
    path('lista-promociones/',views.lista_promociones,name='lista_promociones'),
    path('buscar-promociones/',views.promocion_buscar_avanzado,name='buscar_promociones'),
    path('editar-promocion/<int:promocion_id>/', views.promocion_editar, name='editar_promocion'),
    path('promocion/eliminar/<int:promocion_id>/', views.promocion_eliminar, name='eliminar_promocion'),
    
]