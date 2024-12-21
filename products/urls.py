from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.register, name='register'),
    path('users/login/', views.login, name='login'),
    path('users/current_user/', views.current_user, name='current_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('products/', views.get_products, name='get_products'),
    path('products/<int:product_id>/', views.get_product, name='get_product'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/update/', views.update_product, name='update_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]



