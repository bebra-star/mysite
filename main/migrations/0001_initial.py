# Generated by Django 5.1.1 on 2025-01-02 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('flag', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('language1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language1', to='main.language')),
                ('language2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language2', to='main.language')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='first_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_language', to='main.language'),
        ),
        migrations.AddField(
            model_name='user',
            name='second_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_language', to='main.language'),
        ),
        migrations.CreateModel(
            name='TestSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('current_word_index', models.IntegerField()),
                ('is_showing_language_first', models.BooleanField()),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.dictionary')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WordPair',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('word1', models.CharField(max_length=30)),
                ('word2', models.CharField(max_length=30)),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='TestSessionWordPair',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Skipped'), (1, 'Not Learned'), (2, 'Learned')], default=None, null=True)),
                ('test_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.testsession')),
                ('word_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.wordpair')),
            ],
        ),
    ]
