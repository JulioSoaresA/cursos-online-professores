from django.contrib import admin
from .models import NovoPlano, NovoTopicoAula
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget


class PlanosAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'carga_horaria', 'area_tematica', 'professor_responsavel', 'status')
    list_display_links = ('id', 'titulo', )
    search_fields = ('titulo', )
    readonly_fields = ('id_professor', 'titulo', 'carga_horaria', 'ementa', 'obj_geral', 'area_tematica', 'professor_responsavel', 'data_criacao')
    list_filter = ('titulo', 'area_tematica')
    filter_horizontal = ()
    fieldsets = ()


class TopicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo')
    list_display_links = ('id', 'titulo')
    readonly_fields = ('professor_id', 'plano_curso', 'titulo', 'descricao')
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


admin.site.register(NovoPlano, PlanosAdmin)
admin.site.register(NovoTopicoAula, TopicoAdmin)

