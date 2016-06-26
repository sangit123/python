# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='service_details',
            fields=[
                ('service_id', models.IntegerField(serialize=False, primary_key=True)),
                ('app_name', models.CharField(max_length=100, null=True)),
                ('app_group', models.CharField(max_length=100, null=True)),
                ('group_id', models.CharField(max_length=100, null=True)),
                ('datacenter', models.CharField(max_length=100, null=True)),
                ('hostnames', models.CharField(max_length=100, null=True)),
                ('wily_alert', models.CharField(max_length=100, null=True)),
                ('wily_mom', models.CharField(max_length=100, null=True)),
                ('Spectrum', models.CharField(max_length=100, null=True)),
                ('Sitescope', models.CharField(max_length=100, null=True)),
                ('PagerDuty', models.CharField(max_length=100, null=True)),
                ('P_Services', models.CharField(max_length=100, null=True)),
                ('P_Token', models.CharField(max_length=100, null=True)),
                ('P_SubDomain', models.CharField(max_length=100, null=True)),
                ('Splunk', models.CharField(max_length=100, null=True)),
                ('Wily', models.CharField(max_length=100, null=True)),
                ('NewRelic', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
