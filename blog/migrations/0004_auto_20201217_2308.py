# Generated by Django 3.0.5 on 2020-12-17 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201217_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlehit',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
