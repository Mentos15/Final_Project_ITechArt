# Generated by Django 2.2.6 on 2020-03-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200311_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirencelist',
            name='img',
            field=models.ImageField(blank=True, default='static/images/back2.jpg', null=True, upload_to='static/images'),
        ),
    ]
