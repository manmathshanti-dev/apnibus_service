from common.models.base_model import BaseModel
from django.db import models

from pos_proxy.models import ProxyBus, ProxyBusRoute
from service_app.models.service_model import Service

class TimeTable(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    town_alias = models.CharField(max_length=150,null=True,blank=True)
