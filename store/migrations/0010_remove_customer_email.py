# Generated by Django 5.0.1 on 2024-01-15 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_customer_options_remove_customer_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
    ]
