# Generated by Django 4.2.1 on 2023-05-19 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='اسم الكتاب')),
                ('code', models.IntegerField(verbose_name='الرقم الخاص')),
                ('author', models.CharField(max_length=150, verbose_name='المؤلف')),
                ('category', models.IntegerField(choices=[(200, 'منوعات'), (300, 'الأسرة'), (400, 'الشباب'), (500, 'الخدمة'), (600, 'اللاهوت الروحي'), (700, 'تاريخ الكنيسة وسير الآباء'), (800, 'اللاهوت الطقسي'), (900, 'اللاهوت العقائدي'), (1000, 'الكتاب المقدس'), (2000, 'الموسوعات'), (3000, 'المجلدات')], default=200, verbose_name='الرقم العام')),
                ('count', models.IntegerField(default=1, verbose_name='عدد النسخ')),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='اسم المستعير')),
                ('books', models.ManyToManyField(to='books.book')),
            ],
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.borrower')),
            ],
        ),
    ]
