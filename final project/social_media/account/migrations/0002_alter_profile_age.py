# Generated by Django 4.2.5 on 2023-10-04 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
