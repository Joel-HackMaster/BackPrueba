# Generated by Django 5.0.6 on 2024-07-01 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='photo',
            field=models.TextField(default='photo'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.TextField(default='photo'),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='password',
            field=models.EmailField(max_length=255, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.EmailField(max_length=255, verbose_name='Password'),
        ),
    ]
