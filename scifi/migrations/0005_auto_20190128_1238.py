# Generated by Django 2.1.4 on 2019-01-28 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0004_auto_20190128_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='tranaction_type',
            new_name='transaction_type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='fiscal_year',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]