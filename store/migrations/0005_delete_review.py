# Generated by Django 5.0.4 on 2024-04-27 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_orderitem_product_alter_product_collection_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]