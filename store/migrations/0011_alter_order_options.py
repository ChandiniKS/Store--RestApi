# Generated by Django 5.0.1 on 2024-01-15 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_customer_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel orders')]},
        ),
    ]