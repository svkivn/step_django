from PIL import Image
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)


    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img = Image.open(self.photo.path)
            max_size = (300, 300)  # Максимальний розмір (ширина, висота)
            quality = 85  # Якість зображення (від 1 до 100)

            if img.height > max_size[1] or img.width > max_size[0]:
                img.thumbnail(max_size)
            img.save(self.photo.path, quality=quality)
