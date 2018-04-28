# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMLContentAppBarrapunto', '0002_barrapunto'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Barrapunto',
            new_name='News',
        ),
    ]
