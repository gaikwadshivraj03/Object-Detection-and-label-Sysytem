from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload',views.uploadfiles,name='upload_data'),
    path('report',views.report,name='reportsfile'),
]