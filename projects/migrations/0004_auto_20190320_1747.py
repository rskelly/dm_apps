# Generated by Django 2.1.4 on 2019-03-20 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_delete_fiscalyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='section',
            field=models.ForeignKey(blank=True, limit_choices_to={'division__branch': 1}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='shared_models.Section', verbose_name='section'),
        ),
    ]