# Generated by Django 4.2.6 on 2023-11-17 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_boardtype_name_alter_nodetype_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectboards',
            old_name='parent_sms_board',
            new_name='control_sms_board',
        ),
        migrations.RenameField(
            model_name='projectboards',
            old_name='parent_wifi_board',
            new_name='control_wifi_board',
        ),
        migrations.AlterField(
            model_name='projectboards',
            name='board_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board', to='project.boardtype', verbose_name='برد مربوطه'),
        ),
    ]
