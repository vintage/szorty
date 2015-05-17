# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shortcut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(verbose_name=b'Slug field')),
                ('target_url', models.URLField(verbose_name=b'Redirection URL')),
                ('redirection_count', models.PositiveIntegerField(default=0, verbose_name=b'Redirection count')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Create date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name=b'Last update')),
            ],
            options={
                'verbose_name': 'Redirection URL',
                'verbose_name_plural': 'Redirection URLs',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name=b'Name', db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Create date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name=b'Last update')),
            ],
        ),
        migrations.AddField(
            model_name='shortcut',
            name='word',
            field=models.OneToOneField(verbose_name=b'Matched word', to='shortener.Word'),
        ),
    ]
