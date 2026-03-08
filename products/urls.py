from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.product_list, name='product_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('category/<int:category_id>/update/', views.category_update, name='category_update'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/price-update/', views.price_update, name='price_update'),
    path('<int:pk>/barcode-image/', views.generate_barcode_image, name='barcode_image'),
    path('<int:pk>/barcode-label/', views.print_barcode_label, name='barcode_label'),
    path('barcode-check/', views.barcode_check, name='barcode_check'),
    path('supplies/', views.supply_list, name='supply_list'),
    path('supplies/create/', views.supply_create, name='supply_create'),
    path('supplies/<int:supply_id>/invoice/', views.print_supply_invoice, name='print_supply_invoice'),
]
