# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagerstats_app', '0003_source_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Source_data',
        ),
    ]
