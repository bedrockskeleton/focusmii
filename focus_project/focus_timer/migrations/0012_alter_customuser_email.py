# Generated by Django 5.1.6 on 2025-04-19 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus_timer', '0011_alter_themes_color1_alter_themes_color2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
