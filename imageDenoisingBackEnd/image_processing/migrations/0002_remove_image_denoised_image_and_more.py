# Generated by Django 5.0.6 on 2024-05-28 17:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='denoised_image',
        ),
        migrations.RemoveField(
            model_name='image',
            name='detected_noise',
        ),
        migrations.RemoveField(
            model_name='image',
            name='filter_applied',
        ),
        migrations.RemoveField(
            model_name='image',
            name='noisy_image',
        ),
        migrations.RemoveField(
            model_name='image',
            name='upload_date',
        ),
        migrations.AddField(
            model_name='image',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='image',
            name='original_image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='selected_noise',
            field=models.CharField(max_length=50),
        ),
    ]
