# Generated by Django 2.2.12 on 2020-05-20 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_remove_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='books.Ebook'),
        ),
    ]