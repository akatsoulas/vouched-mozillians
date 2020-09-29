# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0019_auto_20171205_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='is_access_group',
            field=models.BooleanField(default=False, verbose_name=b'Is this an access group?', choices=[(True, 'Access Group'), (False, 'Tag')]),
        ),
    ]
