# Generated by Django 4.2.6 on 2024-03-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_projectscenario_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectscenario',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='نام سناریو'),
        ),
    ]
