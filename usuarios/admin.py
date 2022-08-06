from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuariosAdmin(UserAdmin):
    list_display = ('nome_completo', 'cpf', 'last_login', 'date_joined', 'is_admin', 'is_staff')
    search_fields = ('nome_completo', 'cpf')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Usuario, UsuariosAdmin)
