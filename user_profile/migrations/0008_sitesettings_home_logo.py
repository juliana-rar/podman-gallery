from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_sitesettings_hero_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='home_logo',
            field=models.ImageField(blank=True, null=True, upload_to='site/', verbose_name='Logo del inicio'),
        ),
    ]
