# Generated by Django 3.1.7 on 2021-04-21 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPaperApp', '0007_auto_20210421_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('Новость', 'Новость'), ('Статья', 'Статья')], default='select', max_length=30, verbose_name='Тип'),
        ),
    ]
