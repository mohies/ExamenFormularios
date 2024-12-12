from django.contrib import admin
from .models import *
# Register your models here.
models = [Usuario,Producto,Promocion]

for model in models:    
    admin.site.register(model)