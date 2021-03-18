# Generated by Django 3.1.5 on 2021-03-01 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210225_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.CharField(choices=[('accept', 'accept'), ('decline', 'decline')], default=None, max_length=10)),
            ],
        ),
    ]