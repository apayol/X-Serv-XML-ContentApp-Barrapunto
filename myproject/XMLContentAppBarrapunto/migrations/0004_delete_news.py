# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMLContentAppBarrapunto', '0003_auto_20180428_1550'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
    ]
