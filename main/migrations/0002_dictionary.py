# Generated by Django 5.1.1 on 2024-09-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('language1', models.CharField(max_length=30)),
                ('language2', models.CharField(max_length=30)),
            ],
        ),
    ]