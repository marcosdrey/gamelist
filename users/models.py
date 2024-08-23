from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Usuário")
    profile_photo = models.ImageField(default='default.jpg', upload_to='profile-pics', verbose_name="Foto de Usuário")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
