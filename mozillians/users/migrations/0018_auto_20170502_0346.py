# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20170404_0448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='allows_community_sites',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='allows_mozilla_sites',
        ),
    ]
