from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# create views for main site here

def home(request):
    return render(request, 'reservations/home.html')