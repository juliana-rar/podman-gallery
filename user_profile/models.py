from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "The email must be unique"
        }
    )
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_images"
    )
    followers = models.ManyToManyField("Follow")

    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_profile_picture(self):
        url = ""
        try:
            url = self.profile_image.url
        except:
            url = ""
        return url


class SiteSettings(models.Model):
    """Configuración global del sitio (singleton). Nombres del menú."""
    site_title = models.CharField("Título del sitio", max_length=80, default="Sigfrid")
    favicon = models.ImageField("Logo / favicon", upload_to="site/", null=True, blank=True)
    nav_blogs = models.CharField("Menú · Blogs", max_length=50, default="Eportfolios")
    nav_events = models.CharField("Menú · Events", max_length=50, default="Tips")
    nav_gallery = models.CharField("Menú · Galería", max_length=50, default="Galería")

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return "Configuración del sitio"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Follow(models.Model):
    followed = models.ForeignKey(
        User,
        related_name='user_followers',
        on_delete=models.CASCADE
    )
    followed_by = models.ForeignKey(
        User,
        related_name='user_follows',
        on_delete=models.CASCADE
    )
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed_by.username} started following {self.followed.username}"

