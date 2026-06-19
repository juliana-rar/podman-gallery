from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_sitesettings_home_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='bio_text',
            field=models.TextField(blank=True, default='', verbose_name='Biografía'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='bio_video',
            field=models.FileField(blank=True, null=True, upload_to='site/', verbose_name='Video de la biografía'),
        ),
    ]
