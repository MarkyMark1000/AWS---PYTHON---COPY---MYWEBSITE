# Generated by Django 2.1.1 on 2020-03-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0008_auto_20200308_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcourse',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]