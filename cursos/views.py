from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cursos.forms.planoCursoForm import NovoPlanoCurso
from .models import NovoPlano


def plano_de_curso(request):
    """Cadastra um novo plano de curso"""

    if request.method == 'GET':
        form = NovoPlanoCurso()
        contexto = {'form': form}
        return render(request, 'cursos/plano_de_curso.html', contexto)
    else:
        form = NovoPlanoCurso(request.POST)
        if form.is_valid():
            form = NovoPlanoCurso()
            contexto = {'form': form}
            titulo = request.POST['titulo']
            area_tematica = request.POST['area_tematica']
            carga_horaria = request.POST['carga_horaria']
            ementa = request.POST['ementa']
            obj_geral = request.POST['obj_geral']
            if campo_numerico(carga_horaria):
                messages.error(request, 'Insira um valor numérico.')
            id_professor = request.user.pk
            professor_responsavel = request.user.nome_completo
            novo_plano = NovoPlano.objects.create(id_professor=id_professor, professor_responsavel=professor_responsavel, titulo=titulo, area_tematica_id=area_tematica, carga_horaria=carga_horaria, ementa=ementa, obj_geral=obj_geral, status='AGUARDANDO_AVALIACAO')
            novo_plano.save()
            messages.success(request, 'Novo plano cadastrado com sucesso')
            return render(request, 'cursos/plano_de_curso.html', contexto)
        else:
            contexto = {'form': form}
            return render(request, 'cursos/plano_de_curso.html', contexto)


def campo_numerico(campo):
    return not campo.isnumeric()


def info_curso(request, plano_id):
    curso = get_object_or_404(NovoPlano.objects.all().filter(id=plano_id, id_professor=request.user.pk))
    contexto = {'curso': curso}
    return render(request, 'cursos/info_curso.html', contexto)
