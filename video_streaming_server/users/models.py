from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q



class User(AbstractUser):
    email = models.EmailField(max_length=127, unique=True, blank=False, verbose_name="Email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"



class InterfaceCustomization(models.Model):
    class Meta:
        verbose_name = "Interface Customization"
        verbose_name_plural = "Interface Customization"
        constraints = [models.UniqueConstraint(fields=("title",), condition=Q(active=True), name="unique_active_configuration"),]
    
    title = models.CharField(max_length=127, verbose_name="Title")
    # TODO: Add logo to navbar
    logo = models.ImageField(blank=True, null=True, upload_to="images", verbose_name="Logo")
    active = models.BooleanField(default=True, null=False, verbose_name="Active")
    hide_videos = models.BooleanField(default=False, verbose_name="Hide Videos")

    def __str__(self):
        return f"{self.title}"