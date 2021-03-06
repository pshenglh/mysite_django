# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('pub_date', models.DateField()),
                ('mod_date', models.DateField()),
                ('body_text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_text', models.TextField()),
                ('pub_date', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
    ]
