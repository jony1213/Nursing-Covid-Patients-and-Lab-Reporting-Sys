# Generated by Django 4.0 on 2021-12-13 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_num',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]