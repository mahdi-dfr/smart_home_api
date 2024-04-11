# Generated by Django 4.2.6 on 2024-03-31 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0019_rename_nodeproject_node_board_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectScenario',
            new_name='HardwareScenario',
        ),
        migrations.AlterModelOptions(
            name='hardwarescenario',
            options={'verbose_name': 'سناریو سخت افزاری', 'verbose_name_plural': 'سناریو های سخت افزاری'},
        ),
        migrations.CreateModel(
            name='SoftwareScenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='نام سناریو')),
                ('status', models.CharField(choices=[('0', 'خاموش'), ('1', 'روشن')], default='0', max_length=1, verbose_name='وضعیت سناریو')),
                ('device', models.ManyToManyField(related_name='device_scenario_software', to='project.device', verbose_name='تجهیز')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_scenario_software', to='project.project', verbose_name='پروژه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_scenario_software', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سناریو نرم افزاری',
                'verbose_name_plural': 'سناریو های نرم افزاری',
            },
        ),
    ]