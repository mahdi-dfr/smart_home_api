# Generated by Django 4.2.6 on 2023-11-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_device_event_id_alter_projectscenario_device_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodeproject',
            name='unique_id',
            field=models.SmallIntegerField(blank=True, default=1, verbose_name='شناسه ی نود'),
        ),
        migrations.AlterField(
            model_name='projectboards',
            name='unique_id',
            field=models.SmallIntegerField(blank=True, default=1, verbose_name='شناسه ی برد'),
        ),
    ]
