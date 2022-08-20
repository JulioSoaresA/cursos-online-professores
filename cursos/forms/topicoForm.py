from django import forms
from cursos.models import NovoTopicoAula
from markdownx.widgets import MarkdownxWidget


class NovoTopicoForm(forms.ModelForm):

    class Meta:
        model = NovoTopicoAula
        fields = ['titulo', 'descricao', 'plano_curso']
        labels = {'titulo': 'Título', 'descricao': 'Descrição'}
        exclude = ('professor_id', )
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título',
                'required': 'true'
            }),
            'plano_curso': forms.HiddenInput(),
            'descricao': MarkdownxWidget(attrs={
                'class': 'form-control',
                'required': 'true'
            })
        }


