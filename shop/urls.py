from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('category/<slug:slug>/', views.SubCategories.as_view(), name='category_detail'),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('login_registration/', views.login_registration, name='login_registration'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('register', views.user_registration, name='user_register'),
]
