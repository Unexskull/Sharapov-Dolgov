from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import ServerForm, ServerConfigForm, ServerConnectionConfigForm
from .models import ServerConfig, ServerConnectionConfig
from .monitoringsystem.ssh import SSH
from .utils import extract_cpu_idle, extract_memory_usage, extract_used_memory
from django.http import JsonResponse
from concurrent.futures import ThreadPoolExecutor
# Create your views here.


# кнопки sidebar
def base_view(request):
    return render(request, 'SCS/base.html')

def servers_view(request):
    return render(request, 'SCS/servers.html')

def account_view(request):
    user = request.user
    return render(request, 'SCS/account.html', {'user': user})

def logout_view(request):
    pass
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'SCS/login.html', {'form': form})
    return render(request, 'SCS/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error creating your account.')
    else:
        form = UserCreationForm()
    return render(request, 'SCS/register.html', {'form': form})


#servers
def list_servers_view(request):
    servers = ServerConfig.objects.select_related('server_connection_config').all()
    return render(request, 'SCS/servers.html', {'servers': servers})

def edit_server(request, id):
    server = get_object_or_404(ServerConfig, id=id)
    return render(request, 'edit_server.html', {'server': server})

def delete_server(request, id):
    server = get_object_or_404(ServerConfig, id=id)
    if request.method == 'POST':
        server.delete()
        return redirect('list_servers')
    return render(request, 'confirm_delete.html', {'server': server})

def add_server_view(request):
    form1 = ServerConfigForm()
    form2 = ServerConnectionConfigForm()
    show_form = True
    if request.method == 'POST':
        if request.POST.get('action') == 'add_server_view_submit':
            form1 = ServerConfigForm(request.POST)
            form2 = ServerConnectionConfigForm(request.POST)
            show_form = True
            if form1.is_valid() and form2.is_valid():
                connect = form2.save()
                config = form1.save(commit=False)
                config.user = request.user
                config.server_connection_config = connect
                config.save()
                return redirect('servers')

    return render(request, 'SCS/servers.html', {
        'form1': form1,
        'form2': form2,
        'show_form': show_form,
    })

def ssh_parameters_view(request):
    ssh_parameters = ServerConnectionConfig.objects.all()
    show_ssh = True
    return render(request, 'SCS/servers.html', {'ssh_parameters': ssh_parameters,
                                                                    'show_ssh': show_ssh,
                                                                    })

def server_resource_graph(request):
    servers_name = ServerConfig.objects.filter(is_included=True)
    print(servers_name)
    return render(request, 'SCS/servers.html', {'show_graphic': True,
                                                                    'servers_name': servers_name})

def get_server_data(request):
    if request.method == 'GET':
        server_configs = ServerConfig.objects.filter(is_included=True).select_related('server_connection_config')
        servers_data = {}
        def get_server_info(config):
            try:
                server = {
                    'hostname': config.server_connection_config.ip_address,
                    'username': config.server_connection_config.server_user_name,
                    'password': config.server_connection_config.ssh_password,
                    'port': 22,
                }
                with SSH(**server) as ssh:
                    command = "export TERM=xterm && top -b -n 1"
                    command2 = "export TERM=xterm && df -h"
                    result = ssh.exec_cmd(command)
                    cpu_idle = extract_cpu_idle(result)
                    cpu_load = 100 - int(cpu_idle)
                    result_mem = result.split("\n")
                    memory_usage = extract_memory_usage(result_mem)
                    result2 = ssh.exec_cmd(command2)
                    disk_usage = extract_used_memory(result2)
                    internet_speed = 100  # Заглушка
                    return {
                        f"server_{config.id}": {
                            "cpuLoad": [cpu_load],
                            "memoryLoad": [memory_usage],
                            "diskLoad": [disk_usage],
                            "internetSpeed": [internet_speed]
                        }
                    }
            except Exception as e:
                print(f"Ошибка при подключении к серверу {config.server_name}: {e}")
                return {
                    f"server_{config.id}": {
                        "cpuLoad": ["Ошибка"],
                        "memoryLoad": ["Ошибка"],
                        "diskLoad": ["Ошибка"],
                        "internetSpeed": ["Ошибка"]
                    }
                }
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(get_server_info, server_configs))
        for res in results:
            servers_data.update(res)
        print(servers_data)
        return JsonResponse(servers_data)

