import paramiko

class SSH:
    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.kwargs = kwargs

    def __enter__(self):
        kw = self.kwargs
        self.client.connect(hostname=kw.get('hostname'), username=kw.get('username'), password=kw.get('password'), port=int(kw.get('port', 22)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def exec_cmd(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)

        # Чтение ошибок
        error = stderr.read().decode().strip()
        if error:
            raise Exception(f"Ошибка выполнения команды: {error}")  # Создаем исключение с текстом ошибки

        # Чтение результата
        result = stdout.read().decode().strip()
        return result