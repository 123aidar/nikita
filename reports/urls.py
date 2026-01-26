from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('api/profit-chart/', views.profit_chart_data, name='profit_chart_data'),
    path('api/top-products/', views.top_products_data, name='top_products_data'),
    path('api/top-sellers/', views.top_sellers_data, name='top_sellers_data'),
    path('api/statistics/', views.statistics_data, name='statistics_data'),
    path('api/detailed-sales/', views.detailed_sales_data, name='detailed_sales_data'),
    path('api/detailed-products/', views.detailed_products_data, name='detailed_products_data'),
    path('api/detailed-writeoffs/', views.detailed_writeoffs_data, name='detailed_writeoffs_data'),
]
