# Generated by Django 3.1.3 on 2021-01-29 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_post_liked_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
