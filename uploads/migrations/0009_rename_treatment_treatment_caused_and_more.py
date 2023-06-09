# Generated by Django 4.1.7 on 2023-04-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0008_treatment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treatment',
            old_name='treatment',
            new_name='caused',
        ),
        migrations.AddField(
            model_name='treatment',
            name='chemical_control',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatment',
            name='organic_control',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatment',
            name='preventive_measures',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatment',
            name='symptoms',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
