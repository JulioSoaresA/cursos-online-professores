from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cursos.forms.planoCursoForm import NovoPlanoCurso
from cursos.forms.topicoForm import NovoTopico
from .models import NovoPlano, NovoTopidoAula


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
    """Informações do curso"""

    curso = get_object_or_404(NovoPlano.objects.all().filter(id=plano_id, id_professor=request.user.pk))
    topicos = NovoTopidoAula.objects.filter(plano_curso_id=plano_id, professor_id=request.user.pk).order_by('pk')
    quantidade_topicos = NovoTopidoAula.objects.filter(plano_curso_id=plano_id, professor_id=request.user.pk).count()
    print(quantidade_topicos)
    contexto = {
        'curso': curso,
        'topicos': topicos,
        'quantidade_topicos': quantidade_topicos
    }
    return render(request, 'cursos/info_curso.html', contexto)


def cadastrar_topico(request, plano_id):
    """Cadastra um novo tópico de aula"""

    plano = get_object_or_404(NovoPlano.objects.all().filter(pk=plano_id))
    quantidade_topicos = NovoTopidoAula.objects.all().filter(plano_curso_id=plano_id, professor_id=request.user.pk).count()
    if request.method == 'GET':
        form = NovoTopico()

        contexto = {
            'form': form,
            'plano': plano
        }
        if plano.status == 'REPROVADO':
            messages.error(request, 'Plano RECUSADO, impossível cadastrar tópicos de aula.')
        return render(request, 'cursos/cadastrar_topico.html', contexto)
    else:
        form = NovoTopico()

        contexto = {
            'form': form,
            'plano': plano
        }
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        plano_curso = request.POST.get('plano_curso')

        if quantidade_topicos < 5 and plano.status == 'APROVADO':
            novo_topico = NovoTopidoAula(professor_id=request.user.pk, plano_curso_id=plano_curso, titulo=titulo, descricao=descricao)
            novo_topico.save()
            messages.success(request, 'Tópico de aula cadastrado')
            return render(request, 'cursos/cadastrar_topico.html', contexto)
        elif plano.status == 'REPROVADO':
            messages.error(request, 'Plano RECUSADO, impossível cadastrar tópicos de aula.')
            return render(request, 'cursos/cadastrar_topico.html', contexto)
        else:
            messages.error(request, 'Quantidade máxima de tópicos excedida (MAX: 5 tópicos)')
            return render(request, 'cursos/cadastrar_topico.html', contexto)