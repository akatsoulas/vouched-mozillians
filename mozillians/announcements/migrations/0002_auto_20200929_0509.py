# Generated by Django 2.2.16 on 2020-09-29 12:09

from django.db import migrations, models
import mozillians.announcements.models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, default='', help_text='60x60 pixel image recommended. Image will be rescaled automatically to a square.', upload_to=mozillians.announcements.models._calculate_image_filename),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='publish_from',
            field=models.DateTimeField(help_text='Timezone is America/Los_Angeles'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='publish_until',
            field=models.DateTimeField(blank=True, help_text='Timezone is America/Los_Angeles', null=True),
        ),
    ]
