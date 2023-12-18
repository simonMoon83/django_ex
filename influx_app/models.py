# influx_app/models.py
from django.db import models

class InfluxData(models.Model):
    measurement = models.CharField(max_length=50)
    tag_name = models.CharField(max_length=50)
    tag_value = models.CharField(max_length=50)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)