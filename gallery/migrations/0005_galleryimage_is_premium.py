# Generated for Premium classification

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_galleryimage_paper_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='is_premium',
            field=models.BooleanField(default=False, verbose_name='Premium'),
        ),
    ]
