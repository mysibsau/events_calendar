# Generated by Django 3.2.7 on 2022-08-18 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_alter_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('0', 'Отклоненно'), ('1', 'В обработке'), ('2', 'В ожидании отчета'), ('3', 'Верефицированно')], default='1', max_length=1, verbose_name='Статус Мероприятия'),
        ),
    ]
