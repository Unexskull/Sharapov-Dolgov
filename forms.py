from django import forms
from .models import ServerConfig, ServerConnectionConfig


class ServerConfigForm(forms.ModelForm):
    class Meta:
        model = ServerConfig
        fields = ['server_name', 'is_included']
        labels = {'server_name': 'Имя сервера',
                  'is_included': 'Включен',
                  }


class ServerConnectionConfigForm(forms.ModelForm):
    class Meta:
        model = ServerConnectionConfig
        fields = ['server_user_name', 'ip_address', 'ssh_public_key', 'ssh_password']
        labels = {
            'server_user_name': 'Имя пользователя сервера',
            'ip_address': 'IP-адрес',
            'ssh_public_key': 'Публичный ключ SSH',
            'ssh_password': 'Пароль SSH',
        }

class ServerForm(forms.Form):
    server_config_form = ServerConfigForm()
    server_connection_config_form = ServerConnectionConfigForm()