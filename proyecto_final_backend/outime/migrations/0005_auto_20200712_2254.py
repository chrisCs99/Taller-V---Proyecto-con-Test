# Generated by Django 3.0.7 on 2020-07-13 02:54

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('outime', '0004_auto_20200712_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento_stock',
            name='tipo_movimiento',
            field=django_fsm.FSMIntegerField(choices=[(0, 'Ingreso'), (1, 'Egreso')], default=1, protected=True),
        ),
    ]