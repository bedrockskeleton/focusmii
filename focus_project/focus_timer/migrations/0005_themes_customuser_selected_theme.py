# Generated by Django 5.1.6 on 2025-04-12 04:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus_timer', '0004_timers_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('color1', models.CharField(max_length=6)),
                ('color2', models.CharField(max_length=6)),
                ('color3', models.CharField(max_length=6)),
                ('image', models.ImageField(blank=True, upload_to='themes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='selected_theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='focus_timer.themes'),
        ),
    ]
