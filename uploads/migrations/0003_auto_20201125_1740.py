# Generated by Django 3.0.7 on 2020-11-25 17:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_auto_20201124_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 17, 40, 24, 812039, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 17, 40, 24, 812020, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='creationdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 17, 40, 24, 810202, tzinfo=utc)),
        ),
    ]
