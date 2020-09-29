# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-20 10:05


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_auto_20180704_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalaccount',
            name='type',
            field=models.CharField(choices=[(b'AIM', b'AIM'), (b'BITBUCKET', b'Bitbucket'), (b'BMO', b'Bugzilla (BMO)'), (b'DISCORD', b'Discord'), (b'FACEBOOK', b'Facebook'), (b'LANYRD', b'Lanyrd'), (b'LINKEDIN', b'LinkedIn'), (b'MDN', b'MDN'), (b'MASTODON', b'Mastodon'), (b'AMO', b'Mozilla Add-ons'), (b'DISCOURSE', b'Mozilla Discourse'), (b'MOZILLALOCATION', b'Mozilla Location Service'), (b'MOZPHAB', b'Mozilla Phabricator'), (b'MOZILLAPONTOON', b'Mozilla Pontoon'), (b'REMO', b'Mozilla Reps'), (b'SUMO', b'Mozilla Support'), (b'WEBMAKER', b'Mozilla Webmaker'), (b'MOZILLAWIKI', b'Mozilla Wiki'), (b'Phone (Landline)', b'Phone (Landline)'), (b'Phone (Mobile)', b'Phone (Mobile)'), (b'SKYPE', b'Skype'), (b'SLIDESHARE', b'SlideShare'), (b'TELEGRAM', b'Telegram'), (b'TRANSIFEX', b'Transifex'), (b'TWITTER', b'Twitter'), (b'WEBSITE', b'Website URL'), (b'JABBER', b'XMPP/Jabber'), (b'YAHOO', b'Yahoo! Messenger')], max_length=30, verbose_name='Account Type'),
        ),
    ]
