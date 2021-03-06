# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 09:45
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grad', '0007_auto_20160408_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradstatus',
            name='status',
            field=models.CharField(choices=[(b'INCO', b'Incomplete Application'), (b'COMP', b'Complete Application'), (b'INRE', b'Application In-Review'), (b'HOLD', b'Hold Application'), (b'OFFO', b'Offer Out'), (b'REJE', b'Rejected Application'), (b'DECL', b'Declined Offer'), (b'EXPI', b'Expired Application'), (b'CONF', b'Confirmed Acceptance'), (b'CANC', b'Cancelled Acceptance'), (b'ARIV', b'Arrived'), (b'ACTI', b'Active'), (b'PART', b'Part-Time'), (b'LEAV', b'On-Leave'), (b'WIDR', b'Withdrawn'), (b'GRAD', b'Graduated'), (b'NOND', b'Non-degree'), (b'GONE', b'Gone'), (b'ARSP', b'Completed Special'), (b'TRIN', b'Transferred from another department'), (b'TROU', b'Transferred to another department'), (b'DELE', b'Deleted Record'), (b'DEFR', b'Deferred'), (b'GAPL', b'Applied for Graduation'), (b'GAPR', b'Graduation Approved')], max_length=4),
        ),
        migrations.AlterField(
            model_name='gradstudent',
            name='current_status',
            field=models.CharField(choices=[(b'INCO', b'Incomplete Application'), (b'COMP', b'Complete Application'), (b'INRE', b'Application In-Review'), (b'HOLD', b'Hold Application'), (b'OFFO', b'Offer Out'), (b'REJE', b'Rejected Application'), (b'DECL', b'Declined Offer'), (b'EXPI', b'Expired Application'), (b'CONF', b'Confirmed Acceptance'), (b'CANC', b'Cancelled Acceptance'), (b'ARIV', b'Arrived'), (b'ACTI', b'Active'), (b'PART', b'Part-Time'), (b'LEAV', b'On-Leave'), (b'WIDR', b'Withdrawn'), (b'GRAD', b'Graduated'), (b'NOND', b'Non-degree'), (b'GONE', b'Gone'), (b'ARSP', b'Completed Special'), (b'TRIN', b'Transferred from another department'), (b'TROU', b'Transferred to another department'), (b'DELE', b'Deleted Record'), (b'DEFR', b'Deferred'), (b'GAPL', b'Applied for Graduation'), (b'GAPR', b'Graduation Approved')], db_index=True, help_text=b'Current student status', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='lettertemplate',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'autoslug', unique=True),
        ),
    ]
