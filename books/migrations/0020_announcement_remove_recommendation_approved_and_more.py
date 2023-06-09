# Generated by Django 4.2.1 on 2023-06-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0019_recommendation_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='العنوان')),
                ('text', models.TextField(verbose_name='النص')),
                ('timestamp', models.DateField(auto_now_add=True, verbose_name='التاريخ')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='profile',
        ),
    ]
