# Generated by Django 4.0.1 on 2022-04-21 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Remember', '0009_alter_patient_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.BinaryField(max_length=200),
        ),
    ]