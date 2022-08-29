# Generated by Django 3.2.7 on 2022-08-29 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_delete_importantdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('stop_date', models.DateField(blank=True, verbose_name='Дата окончания')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.eventgroup'),
        ),
    ]
