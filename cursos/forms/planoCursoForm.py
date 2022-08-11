from django import forms
from cursos.models import NovoPlano, AreaTematica


class NovoPlanoForm(forms.ModelForm):
    area_tematica = forms.ModelChoiceField(queryset=AreaTematica.objects.all())
    class Meta:
        model = NovoPlano
        fields = '__all__'
        exclude = ('id_professor', 'professor_responsavel', 'status', 'data_criacao')
        labels = {'titulo': 'Título',
                  'area_tematica': 'Área temática',
                  'carga_horaria': 'Carga horária',
                  'ementa': 'Ementa',
                  'obj_geral': 'Objetivo geral'}
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título',
                'required': 'true'
            }),
            'carga_horaria': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'true'
            }),
            'ementa': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'obj_geral': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'true'
            })
        }

    field_order = ['titulo', 'area_tematica', 'carga_horaria', 'data_nascimento', 'ementa']


