from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class nfc_Info(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    uid_card = models.CharField(max_length=50)
    credit = models.BigIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.uid_card} - {self.date} - {self.credit}"