from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_exhibition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesettings',
            old_name='nav_events',
            new_name='nav_miscellany',
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='nav_miscellany',
            field=models.CharField(default='Tips', max_length=50, verbose_name='Menú · Miscellany'),
        ),
    ]
