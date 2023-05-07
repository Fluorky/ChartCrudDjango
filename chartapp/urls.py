from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart, name='index'),
    path('add', views.addData),
    path('products', views.list_view),
    path('<id>/update', views.update_view),
    path('<id>', views.detail_view),
    path('name/<category>', views.detail_view_by_name),
    path('<id>/delete', views.delete_view),

]
