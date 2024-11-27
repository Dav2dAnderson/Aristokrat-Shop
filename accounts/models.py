from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)

    def __str__(self) -> str:
        return self.fullname
    



