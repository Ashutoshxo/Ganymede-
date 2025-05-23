# Generated by Django 5.1.2 on 2025-01-29 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ganymede', '0002_delete_musicx'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['genre', '-release_date']},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
