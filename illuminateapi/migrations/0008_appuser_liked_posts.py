# Generated by Django 4.0.3 on 2022-03-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('illuminateapi', '0007_appuser_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='liked_posts',
            field=models.ManyToManyField(related_name='liked_by', to='illuminateapi.post'),
        ),
    ]
