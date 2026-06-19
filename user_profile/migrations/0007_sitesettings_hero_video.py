from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_sitesettings_instagram_url_sitesettings_tiktok_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='hero_video',
            field=models.FileField(blank=True, null=True, upload_to='site/', verbose_name='Video del hero'),
        ),
    ]
