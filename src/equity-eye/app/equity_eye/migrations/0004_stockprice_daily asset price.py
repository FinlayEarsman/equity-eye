# Generated by Django 4.1.6 on 2023-02-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equity_eye', '0003_alter_article_assets_alter_article_published'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='stockprice',
            constraint=models.UniqueConstraint(fields=('time', 'asset'),
                                               name='daily asset price'),
        ),
    ]
