# Generated by Django 3.0.3 on 2020-08-10 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcctv', '0005_auto_20200730_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('re_password', models.CharField(max_length=200)),
            ],
        ),
    ]
