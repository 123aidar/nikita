from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('write-offs/', views.write_off_list, name='write_off_list'),
    path('write-offs/create/', views.write_off_create, name='write_off_create'),
    path('inventories/', views.inventory_list, name='inventory_list'),
    path('inventories/create/', views.inventory_create, name='inventory_create'),
    path('inventories/report/<str:session_id>/', views.print_inventory_report, name='print_inventory_report'),
    path('inventories/send-email/<str:session_id>/', views.send_inventory_email, name='send_inventory_email'),
]

