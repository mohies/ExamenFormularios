from django.shortcuts import render,redirect
from .models import *
from django.db.models import Prefetch,Count,Q
from .forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')