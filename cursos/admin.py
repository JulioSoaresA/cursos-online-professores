from django.contrib import admin
from .models import NovoPlano


class PlanosAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'carga_horaria', 'area_tematica', 'professor_responsavel', 'status')
    list_display_links = ('id', 'titulo', )
    readonly_fields = ('id_professor', 'titulo', 'carga_horaria', 'ementa', 'obj_geral', 'area_tematica', 'professor_responsavel')
    list_filter = ('titulo', 'area_tematica')
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(NovoPlano, PlanosAdmin)
