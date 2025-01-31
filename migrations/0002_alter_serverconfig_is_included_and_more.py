# Generated by Django 5.1.5 on 2025-01-24 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SCS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverconfig',
            name='is_included',
            field=models.BooleanField(default=False, verbose_name='Включен'),
        ),
        migrations.AlterField(
            model_name='serverconfig',
            name='server_name',
            field=models.CharField(max_length=32, verbose_name='Имя сервера'),
        ),
        migrations.AlterField(
            model_name='serverconnectionconfig',
            name='ip_address',
            field=models.CharField(max_length=32, verbose_name='IP-адресс сервера'),
        ),
        migrations.AlterField(
            model_name='serverconnectionconfig',
            name='server_user_name',
            field=models.CharField(max_length=32, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='serverconnectionconfig',
            name='ssh_password',
            field=models.CharField(max_length=512, null=True, verbose_name='SSH пароль'),
        ),
        migrations.AlterField(
            model_name='serverconnectionconfig',
            name='ssh_public_key',
            field=models.CharField(max_length=512, null=True, verbose_name='SSH ключ'),
        ),
    ]
