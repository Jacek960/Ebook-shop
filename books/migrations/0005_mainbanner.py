# Generated by Django 2.2.12 on 2020-05-09 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('image', models.ImageField(upload_to='books/static/img/baner/')),
                ('url', models.CharField(max_length=350)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]