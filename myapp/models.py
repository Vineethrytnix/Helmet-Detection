from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)
    
class Userreg(models.Model):
    name=models.CharField(max_length=100, null=True)   
    email=models.EmailField(max_length=100, null=True)   
    phone=models.IntegerField(null=True)   
    address=models.CharField(max_length=100, null=True)   
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)  
    
class Helmet(models.Model):
    uid=models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True)
    rider=models.FileField(upload_to="posts",null=True, blank=True)
    numberplate=models.FileField(upload_to="posts",null=True, blank=True)