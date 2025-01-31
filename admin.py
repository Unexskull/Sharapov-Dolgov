from django.contrib import admin
from SCS.models import ServerConfig, ServerConnectionConfig

# Register your models here.

class ServerConnectionConfigAdmin(admin.ModelAdmin):
    list_display = ('server_user_name', 'ip_address', 'ssh_public_key', 'ssh_password')
    list_filter = ('server_user_name', 'ip_address')
    search_fields = ('server_user_name', 'ip_address')
admin.site.register(ServerConnectionConfig, ServerConnectionConfigAdmin)

class ServerConfigAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'server_connection_config', 'is_included')
    list_filter = ('server_name', 'is_included')
    search_fields = ('server_name', 'is_included')
admin.site.register(ServerConfig, ServerConfigAdmin)