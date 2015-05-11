# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagerstats_app', '0004_delete_source_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source_data',
            fields=[
                ('source_date', models.DateTimeField(serialize=False, primary_key=True)),
                ('open_date', models.CharField(max_length=100, null=True)),
                ('close_date', models.CharField(max_length=100, null=True)),
                ('group_date', models.DateField(null=True)),
                ('service_name', models.CharField(max_length=100, null=True)),
                ('shift', models.CharField(max_length=10, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('resolved_by', models.CharField(max_length=100, null=True)),
                ('escalations', models.CharField(max_length=10, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('domain', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
