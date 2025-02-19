from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Product, Category


class Index(ListView):
    """Главная страница"""
    model = Product
    extra_context = {'title': 'Главная страница'}
    template_name = 'shop/index.html'

