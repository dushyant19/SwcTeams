from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUser(AbstractUser) :
    username = models.CharField(max_length=255,unique=True,blank=True,null=True)
    email = models.EmailField(max_length=255,unique=True,blank=True,null=True) 
    last_name = models.CharField(max_length=255,blank=True,null=True)
    first_name = models.CharField(max_length=255,blank=True,null=True) 

    def __str__(self) :
        return self.username 


#contact,image,status,gender,dateodbirth
class Profile(models.Model) :

    class Gender(models.TextChoices) :
        FEMALE = 'F',_("female")
        MALE = "M",_("male")  

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    pic          = models.ImageField(upload_to='profile_pics/',default='')
    gender       = models.CharField(max_length=30,choices=Gender.choices,blank=True)
    created_at = models.DateTimeField(auto_now=False,auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 


@receiver(post_save,sender=settings.AUTH_USER_MODEL) 
def create_profile(sender,instance,created,**kwargs) :
   if created :
       Profile.objects.create(user=instance)