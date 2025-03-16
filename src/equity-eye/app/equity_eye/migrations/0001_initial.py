# Generated by Django 4.1.4 on 2022-12-20 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(blank=True, max_length=80,
                                            null=True)),
                ('source', models.CharField(blank=True, max_length=80,
                                            null=True)),
                ('body', models.TextField(default='', max_length=15500)),
                ('imported', models.DateField(auto_now_add=True)),
                ('published', models.DateField(auto_now_add=True)),
                ('url', models.URLField(unique=True)),
            ],
            options={
                'ordering': ('-imported',),
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('summary',
                 models.CharField(blank=True, max_length=10000, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('time', models.DateTimeField(db_index=True)),
                ('open', models.DecimalField(decimal_places=6, max_digits=20)),
                ('close', models.DecimalField(decimal_places=6,
                                              max_digits=20)),
                ('high', models.DecimalField(decimal_places=6, max_digits=20)),
                ('low', models.DecimalField(decimal_places=6, max_digits=20)),
                ('volume',
                 models.DecimalField(decimal_places=6, max_digits=20)),
                ('asset',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='prices',
                                   to='equity_eye.asset')),
            ],
        ),
    ]
