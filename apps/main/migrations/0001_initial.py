# Generated by Django 2.0 on 2018-05-21 04:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255)),
                ('url', models.URLField(db_index=True, max_length=400, unique=True)),
                ('img', models.URLField(blank=True, max_length=400, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('domain', models.CharField(max_length=255)),
            ],
        ),
    ]
