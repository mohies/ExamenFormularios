from django.db import models


class Usuario(models.Model):    
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    puede_tener_promociones = models.BooleanField()

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE) #una promocion tiene un producto y un producto puede tener varias promociones
    usuarios = models.ManyToManyField(Usuario,related_name="promocion_usuario") #un usuario  puede tener varias promociones y varias promociones pueden estar asociada a usuarios
    fecha_inicio = models.DateField()  
    fecha_fin = models.DateField() 
    descuento=models.IntegerField()
    esta_activa = models.BooleanField(default=True) 




