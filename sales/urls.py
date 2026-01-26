from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.sale_list, name='sale_list'),
    path('create/', views.sale_create, name='sale_create'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('<int:pk>/print/', views.print_receipt, name='print_receipt'),
    path('api/product/<int:product_id>/', views.get_product_info, name='get_product_info'),
]
