# influxdb_example/influx_app/urls.py
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
]
