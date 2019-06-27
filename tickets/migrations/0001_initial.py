# Generated by Django 2.1.4 on 2019-03-22 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tickets.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to=tickets.models.ticket_directory_path)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(blank=True, max_length=225, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(max_length=255)),
                ('financial_follow_up_needed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['request_type'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name (English)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name (French)')),
                ('color', models.CharField(blank=True, max_length=25, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('priority', models.CharField(choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Wish List'), ('5', 'Urgent')], default='2', max_length=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('financial_coding', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('notes_html', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('date_opened', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_closed', models.DateTimeField(blank=True, null=True)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('people_notes', models.TextField(blank=True, null=True)),
                ('resolved_email_date', models.DateTimeField(blank=True, null=True, verbose_name='Notification sent to primary contact')),
                ('sd_ref_number', models.CharField(blank=True, max_length=8, null=True, verbose_name='Service desk reference #')),
                ('sd_ticket_url', models.URLField(blank=True, null=True, verbose_name='Service desk ticket URL')),
                ('sd_description', models.TextField(blank=True, null=True, verbose_name='Service desk ticket description')),
                ('sd_date_logged', models.DateTimeField(blank=True, null=True, verbose_name='Service desk date logged')),
                ('financial_follow_up_needed', models.BooleanField(default=False)),
                ('estimated_cost', models.FloatField(blank=True, null=True)),
                ('fiscal_year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.FiscalYear')),
                ('primary_contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('request_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.RequestType')),
                ('sd_primary_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sd_tickets_persons', to=settings.AUTH_USER_MODEL, verbose_name='Service desk primary contact')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.Section')),
                ('status', models.ForeignKey(default=2, on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.Status')),
            ],
            options={
                'ordering': ['status', '-date_modified'],
            },
        ),
        migrations.AddField(
            model_name='file',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='tickets.Ticket'),
        ),
    ]