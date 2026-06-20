from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_biophoto_sitesettings_bio_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='hero_text',
            field=models.TextField(blank=True, default='', verbose_name='Texto bajo el hero'),
        ),
    ]
