# Generated by Django 4.2.1 on 2023-06-10 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_profile_name_post_approved_profile_user'),
        ('books', '0011_delete_post_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='age_category',
            field=models.IntegerField(blank=True, choices=[(1, 'حضانة'), (2, 'ابتدائي'), (3, 'اعدادي'), (4, 'ثانوي'), (5, 'الشباب'), (6, 'الأسرة')], null=True, verbose_name='الفئة العمرية'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.profile', verbose_name='المستعير'),
        ),
        migrations.DeleteModel(
            name='Borrower',
        ),
    ]
