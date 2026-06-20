# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_galleryimage_is_premium'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='is_public',
            field=models.BooleanField(
                default=True,
                help_text='Si se desactiva, la obra no aparece en /gallery',
                verbose_name='Visible en la galería',
            ),
        ),
    ]
