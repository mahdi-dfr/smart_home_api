# Generated by Django 4.2.6 on 2023-12-15 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_nodeproject_unique_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='event_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='رویداد'),
        ),
    ]