# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-06 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarkdownPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('md_filename', models.CharField(max_length=100)),
                ('html_content', models.TextField(blank=True, editable=False, null=True)),
            ],
        ),
    ]
