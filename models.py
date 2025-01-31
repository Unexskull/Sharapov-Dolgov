from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField

# Create your models here.

class ServerConnectionConfig(models.Model):
    server_user_name = CharField(max_length=32, verbose_name='Имя пользователя')
    ip_address = CharField(max_length=32, verbose_name='IP-адресс сервера')
    ssh_public_key = CharField(max_length=512, null=True, verbose_name='SSH ключ')
    ssh_password = CharField(max_length=512, null=True, verbose_name='SSH пароль')

    def __str__(self):
        return f"{self.server_user_name} - {self.ip_address}"

    class Meta:
        verbose_name = "Server Connection Configuration"
        verbose_name_plural = "Server Connection Configurations"
        ordering = ['id']

class ServerConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='server_config')
    server_name = CharField(max_length=32, verbose_name='Имя сервера')
    server_connection_config = models.ForeignKey(ServerConnectionConfig, on_delete=models.CASCADE, related_name="server_config")
    is_included = models.BooleanField(default=False, verbose_name='Включен')

    def __str__(self):
        return f"User: {self.user.username}, Server Name: {self.server_name}, Connection: {self.server_connection_config}, Included: {self.is_included}"

    class Meta:
        verbose_name = "Server Configuration"
        verbose_name_plural = "Server Configurations"
        ordering = ['server_name']