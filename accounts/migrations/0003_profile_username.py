# Generated by Django 3.1.7 on 2021-04-05 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210404_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]