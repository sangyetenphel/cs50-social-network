# Generated by Django 3.1.3 on 2021-01-17 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20210117_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfollowing',
            name='following',
        ),
        migrations.AddField(
            model_name='userfollowing',
            name='following',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
