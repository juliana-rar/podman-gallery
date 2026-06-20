# Generated for Exhibitions feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_sitesettings_hero_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exhibition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('location', models.CharField(blank=True, help_text='Galería, sala o ciudad', max_length=200, verbose_name='Lugar')),
                ('start_date', models.DateField(verbose_name='Fecha de inicio')),
                ('end_date', models.DateField(blank=True, help_text='Déjalo vacío si es un solo día', null=True, verbose_name='Fecha de fin')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('url', models.URLField(blank=True, verbose_name='Enlace (opcional)')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Exhibición',
                'verbose_name_plural': 'Exhibiciones',
                'ordering': ['start_date'],
            },
        ),
    ]
