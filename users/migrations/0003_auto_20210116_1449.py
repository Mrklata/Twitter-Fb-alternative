# Generated by Django 3.1.5 on 2021-01-16 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210116_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='stars',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
