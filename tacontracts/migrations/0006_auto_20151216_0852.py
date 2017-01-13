# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tacontracts', '0005_autoslug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tacontract',
            name='appointment_end',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tacontract',
            name='appointment_start',
            field=models.DateField(null=True, blank=True),
        ),
    ]
