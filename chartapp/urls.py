from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('getdata', views.chart, name='ind'),
    path('add', views.addData),
    path('products', views.list_view),
    path('<id>/update', views.update_view),
    path('<int:id>', views.detail_view),
    path('name/<category>', views.detail_view_by_name),
    path('<int:id>/delete', views.delete_view),
    path('autoupdate', views.products_chart),
    #path('', views.home, name='home'),
    path('products-chart/', views.products_chart, name='products-chart'),

]
