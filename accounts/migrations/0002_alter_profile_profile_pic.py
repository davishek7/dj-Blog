# Generated by Django 3.2 on 2021-04-12 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pic.png', null=True, upload_to='profile_pics'),
        ),
    ]
