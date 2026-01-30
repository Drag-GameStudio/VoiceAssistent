from django.db import models

class Dialog(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
