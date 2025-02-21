from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Product, Category
from .forms import LoginForm, RegistrationForm


class Index(ListView):
    """Главная страница"""
    model = Product
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}
    template_name = 'shop/index.html'

    def get_queryset(self):
        """Вывод родительских категорий"""
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение рекомендуемых товаров"""
        context = super().get_context_data()    # context = {}
        context['top_products'] = Product.objects.order_by('-watched')[:8]
        return context


class SubCategories(ListView):
    """Вывод подкатегорий на отдельной странице"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        """
        Возвращает queryset продуктов, отфильтрованных по типу, сортировке или подкатегории.

        Если в запросе присутствует параметр 'type', то возвращаются продукты, принадлежащие к категории с указанным slug.
        Если в запросе присутствует параметр 'sort', то возвращаются продукты, отсортированные по указанному полю.
        В противном случае возвращаются продукты, принадлежащие к подкатегориям указанной категории.

        Returns:
            QuerySet: queryset продуктов, отфильтрованных по типу, сортировке или подкатегории.
        """
        type_fields = self.request.GET.get('type')
        if type_fields:
            products = Product.objects.filter(category__slug=type_fields)
            return products

        sort_fields = self.request.GET.get('sort')
        if sort_fields:
            products = Product.objects.order_by(sort_fields)
            return products

        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategories).order_by('?')

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст данных для шаблона."""
        context = super().get_context_data()
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context


class ProductDetail(DetailView):
    """Страница с детальной информацией о товаре."""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/produst_detail.html'

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов"""
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = product.title
        products = Product.objects.filter(category=product.category).exclude(slug=product.slug)[:4]
        context['products'] = products

        return context


def login_registration(request):
    context = {
        'title': 'Войти ил зарегистрироваться',
        'login_form': LoginForm,
        'registration_form': RegistrationForm,
    }

    return render(request, 'shop/login_registration.html', context)


def user_login(request):
    """Аутентификация пользователя"""
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'Вы успешно авторизовались')
        return redirect('index')
    else:
        messages.error(request, 'Ошибка авторизации')
        return redirect('login_registration')


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')


def user_registration(request):
    """Регистрация пользователя"""
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Аккаунт успешно создан')
        return redirect('index')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
        return redirect('login_registration')
