# Generated by Django 2.2.2 on 2020-05-07 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0002_auto_20200503_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='PAAItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='code')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
    ]
