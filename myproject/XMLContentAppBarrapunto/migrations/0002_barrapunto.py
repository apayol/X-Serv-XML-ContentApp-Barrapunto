# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMLContentAppBarrapunto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrapunto',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=280)),
                ('link', models.TextField()),
            ],
        ),
    ]
