# Generated by Django 3.1.3 on 2020-12-16 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weibo-auth', '0004_auto_20201216_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weiboaccount',
            name='user_ability',
            field=models.BigIntegerField(),
        ),
    ]