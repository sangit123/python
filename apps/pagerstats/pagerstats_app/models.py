from django.db import models
import datetime

# Create your models here.
class Source_data(models.Model):
    source_date = models.DateTimeField(primary_key=True) 
    open_date = models.CharField(max_length=100,null=True)
    close_date = models.CharField(max_length=100,null=True)
    group_date = models.DateField(null=True)
    service_name = models.CharField(max_length=100,null=True)
    shift = models.CharField(max_length=10,null=True)
    description = models.CharField(max_length=100,null=True)
    resolved_by = models.CharField(max_length=100,null=True)
    escalations = models.CharField(max_length=10,null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    domain = models.CharField(max_length=100,null=True)