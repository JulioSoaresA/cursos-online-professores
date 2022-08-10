from django.contrib import admin
from django.db import models
from .models import NovoPlano, NovoTopidoAula
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget


class PlanosAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'carga_horaria', 'area_tematica', 'professor_responsavel', 'status')
    list_display_links = ('id', 'titulo', )
    readonly_fields = ('id_professor', 'titulo', 'carga_horaria', 'ementa', 'obj_geral', 'area_tematica', 'professor_responsavel')
    list_filter = ('titulo', 'area_tematica')
    filter_horizontal = ()
    fieldsets = ()


class TopicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo')
    list_display_links = ('id', 'titulo')
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


admin.site.register(NovoPlano, PlanosAdmin)
admin.site.register(NovoTopidoAula, TopicoAdmin)
