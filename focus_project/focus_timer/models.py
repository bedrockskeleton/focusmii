# focus_timer/models.py
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    pass
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    selected_theme = models.ForeignKey('Themes', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()

# models.py
class Timers(models.Model):
    title = models.CharField(max_length=100)
    focus = models.IntegerField(default=25) # Focus time in minutes
    rest = models.IntegerField(default=5) # Rest time in minutes
    uuid = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    color = models.IntegerField(default=0) # 0-5 for each color profile

def user_path(path, instance, filename):
    return 'user_{0}/{1}{2}'.format(instance.user.id, path, filename) 

class Themes(models.Model):
    title = models.CharField(max_length=100)
    # Theme will either store color data or an image
    color1 = models.CharField(max_length=7, blank=True) # Multiple color fields to store either color or gradient data (can easily be passed to page styling)
    color2 = models.CharField(max_length=7, blank=True)
    color3 = models.CharField(max_length=7, blank=True)

    image = models.ImageField(upload_to = 'themes/', blank=True) # Image field to store optional images (passed to page background)
    
    created_at = models.DateTimeField(auto_now_add=True) # Attach a date to entry for sorting

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='themes', default=None)

    def __str__(self):
        return self.title

    def color_list(self):
        colors = [self.color1] + [c for c in [self.color2, self.color3] if c != "#000000"]
        print(colors)
        return colors
    
    def is_color_theme(self):
        return self.color_list() and not self.image

    def is_image_theme(self):
        return bool(self.image)

    
    def get_image(self):
        return self.image