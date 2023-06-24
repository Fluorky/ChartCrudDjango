from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    #path('', views.chart, name='index'),
    path('', views.home, name='index'),
    path('getdata', views.chart, name='ind'),
    path('autoupdate', views.products_chart),
    path('products-chart/', views.products_chart, name='products-chart'),

    path('add', views.addData),
    path('products', views.list_view),
    path('logs',views.log_list_view),
    path('reset', views.reset_view),
    path('<int:id>/reset', views.resetOne),
    path('<int:id>/update', views.update_view),
    path('<int:id>', views.detail_view),
    path('name/<str:category>', views.detail_view_by_name),
    path('<int:id>/delete', views.delete_view),
    path('<int:id>/iterator', views.addOne),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')))

]
