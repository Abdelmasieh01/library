# Generated by Django 4.2.1 on 2023-06-10 11:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_book_image_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='التاريخ'),
            preserve_default=False,
        ),
    ]