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
    hero_video = models.FileField("Video del hero", upload_to="site/", null=True, blank=True)
    hero_text = models.TextField("Texto bajo el hero", blank=True, default="")
    home_logo = models.ImageField("Logo del inicio", upload_to="site/", null=True, blank=True)
    bio_text = models.TextField("Biografía", blank=True, default="")
    bio_video = models.FileField("Video de la biografía", upload_to="site/", null=True, blank=True)
    bio_photo = models.ImageField("Foto de la biografía", upload_to="site/", null=True, blank=True)
    nav_blogs = models.CharField("Menú · Blogs", max_length=50, default="Eportfolios")
    nav_events = models.CharField("Menú · Events", max_length=50, default="Tips")
    nav_gallery = models.CharField("Menú · Galería", max_length=50, default="Galería")
    accent_color = models.CharField("Color de acento", max_length=7, default="#c2a878")
    instagram_url = models.URLField("Instagram", blank=True, default="")
    tiktok_url = models.URLField("TikTok", blank=True, default="")

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


class BioPhoto(models.Model):
    """Foto del 'Contenido destacado' de la página de biografía."""
    image = models.ImageField(upload_to='bio/')
    caption = models.CharField("Texto", max_length=200, blank=True)
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Visible", default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_date']
        verbose_name = "Foto de la biografía"
        verbose_name_plural = "Fotos de la biografía"

    def __str__(self):
        return self.caption or f"BioPhoto #{self.pk}"

