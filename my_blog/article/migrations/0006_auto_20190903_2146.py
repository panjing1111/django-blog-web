# Generated by Django 2.2.4 on 2019-09-03 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20190902_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='total_views',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
