# Generated by Django 5.1.1 on 2024-09-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_dictionary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
