# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from .slugs import generate_unique_slug  
from user_profile.models import User

class EventCategory(models.Model): 
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Event(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_events',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        EventCategory,
        related_name='category_events',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    description = RichTextField()
 
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  
            from events.slugs import generate_unique_slug
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs) 