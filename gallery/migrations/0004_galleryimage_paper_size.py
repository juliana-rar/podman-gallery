# Generated for Tamaño de papel field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_alter_galleryimage_options_galleryimage_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='paper_size',
            field=models.CharField(blank=True, help_text='Ej. A3 (29,7 × 42 cm)', max_length=100, verbose_name='Tamaño de papel'),
        ),
    ]
