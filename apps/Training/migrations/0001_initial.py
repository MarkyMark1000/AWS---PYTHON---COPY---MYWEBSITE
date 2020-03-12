# Generated by Django 2.1.1 on 2020-01-27 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('img', models.CharField(max_length=50)),
                ('main_text', models.TextField(blank=True, default='main training course description ...', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
                ('img', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Training.TrainingGroup'),
        ),
    ]
