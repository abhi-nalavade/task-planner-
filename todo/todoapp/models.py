from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=50)
    detail=models.CharField(max_length=200)
    cat=models.CharField(max_length=20)
    status=models.IntegerField()
    enddate=models.DateField()
    is_deleted=models.BooleanField(default=False)
    created_on=models.DateField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')

