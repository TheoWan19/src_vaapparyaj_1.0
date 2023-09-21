# Generated by Django 4.2.5 on 2023-09-18 11:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_alter_invoice_invoice_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.UUIDField(default=uuid.UUID('e9424eef-ddb0-4cd7-8c1f-3745b74612c0'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(choices=[('R', 'RECEIPT'), ('I', 'INVOICE')], max_length=1),
        ),
    ]