from common.models.base_model import BaseModel
from django.db import models

from pos_proxy.models import ProxyBus, ProxyBusRoute

class Service(BaseModel):
    bus = models.ForeignKey(ProxyBus, on_delete=models.SET_NULL, null=True, blank=True)
    busroute = models.ForeignKey(ProxyBusRoute, on_delete=models.SET_NULL, null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    is_active = models.BooleanField(default=False,null=True,blank=True)
    is_verified = models.BooleanField(default=False, null=True,blank=True)
