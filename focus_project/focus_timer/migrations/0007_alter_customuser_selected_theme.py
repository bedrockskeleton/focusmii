# Generated by Django 5.1.6 on 2025-04-12 23:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus_timer', '0006_themes_user_alter_customuser_selected_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='selected_theme',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='focus_timer.themes'),
        ),
    ]
