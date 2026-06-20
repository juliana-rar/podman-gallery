# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_galleryimage_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='is_featured',
            field=models.BooleanField(
                default=False,
                help_text='Si se activa, la obra aparece en el carrusel destacado de /biografia',
                verbose_name='Contenido destacado',
            ),
        ),
    ]
