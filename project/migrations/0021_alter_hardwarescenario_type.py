# Generated by Django 4.2.6 on 2024-04-15 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_rename_projectscenario_hardwarescenario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardwarescenario',
            name='type',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True, verbose_name='نوع'),
        ),
    ]