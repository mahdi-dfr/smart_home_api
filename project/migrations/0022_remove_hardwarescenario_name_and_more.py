# Generated by Django 4.2.6 on 2024-05-03 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_alter_hardwarescenario_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hardwarescenario',
            name='name',
        ),
        migrations.AddField(
            model_name='softwarescenario',
            name='unique_id',
            field=models.SmallIntegerField(blank=True, default=1, verbose_name='شناسه ی سناریو'),
        ),
    ]
