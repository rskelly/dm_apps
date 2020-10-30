# Generated by Django 3.1.2 on 2020-10-28 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0019_auto_20201028_1106'),
        ('cruises', '0005_delete_cruiseinstruments'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='cruise',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='instruments', to='shared_models.cruise'),
            preserve_default=False,
        ),
    ]