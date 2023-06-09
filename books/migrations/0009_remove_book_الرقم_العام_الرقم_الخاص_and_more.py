# Generated by Django 4.2.1 on 2023-05-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_book_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='book',
            name='الرقم العام - الرقم الخاص',
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('category', 'code'), name='unique_category_code'),
        ),
    ]
