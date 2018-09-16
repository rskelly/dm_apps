# Generated by Django 2.0.4 on 2018-09-12 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0027_auto_20180912_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='fishdetailtest',
            name='field_name',
            field=models.CharField(choices=[('1', 'Global'), ('3', 'Somatic weight'), ('4', 'Gonad weight'), ('2', 'Fish length')], default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='test',
            name='scope',
            field=models.IntegerField(choices=[(2, 'Global'), (1, 'Data point')]),
        ),
    ]