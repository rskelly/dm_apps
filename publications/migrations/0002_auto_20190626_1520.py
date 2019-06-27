# Generated by Django 2.2.2 on 2019-06-26 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organization(s)',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ManyToManyField(to='publications.Organization', verbose_name='Organization(s)'),
        ),
    ]
