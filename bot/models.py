from django.db import models

# Create your models here.
class User(models.Model):
    external_id=models.IntegerField(unique=True)
    username=models.CharField(max_length=255,blank=True,null=True)
    name=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.name} {self.username} {self.external_id} " 

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    text=models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='posts/',blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.user}"


