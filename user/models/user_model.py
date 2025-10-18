from common.models.base_model import BaseModel
from django.db import models

class User(BaseModel):
    user_name = models.CharField(max_length=30,null=True,blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True,blank=True)
    is_verified = models.BooleanField(default=False,null=True,blank=True)
