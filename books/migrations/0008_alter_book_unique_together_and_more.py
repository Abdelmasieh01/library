# Generated by Django 4.2.1 on 2023-05-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_book_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('category', 'code'), name='الرقم العام - الرقم الخاص'),
        ),
    ]
