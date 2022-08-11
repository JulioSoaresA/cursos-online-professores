from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cursos.forms.planoCursoForm import NovoPlanoForm
from cursos.forms.topicoForm import NovoTopico
from .models import NovoPlano, NovoTopicoAula, TokenValidacao, TokenCertificado
from cursos.forms.captchaForm import CaptchaForm
from datetime import datetime
import secrets
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import json
import requests


def plano_de_curso(request):
    """Cadastra um novo plano de curso"""

    if request.method == 'GET':
        form = NovoPlanoForm()
        contexto = {'form': form}
        return render(request, 'cursos/plano_de_curso.html', contexto)
    else:
        form = NovoPlanoForm(request.POST)
        if form.is_valid():

            form = NovoPlanoForm()

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
            novo_plano = NovoPlano.objects.create(id_professor=id_professor, professor_responsavel=professor_responsavel, titulo=titulo, area_tematica_id=area_tematica, carga_horaria=carga_horaria, ementa=ementa, obj_geral=obj_geral, status='AGUARDANDO_AVALIACAO', data_criacao=datetime.now())
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
    topicos = NovoTopicoAula.objects.filter(plano_curso_id=plano_id, professor_id=request.user.pk).order_by('pk')
    quantidade_topicos = NovoTopicoAula.objects.filter(plano_curso_id=plano_id, professor_id=request.user.pk).count()

    contexto = {
        'curso': curso,
        'topicos': topicos,
        'quantidade_topicos': quantidade_topicos
    }
    return render(request, 'cursos/info_curso.html', contexto)


def cadastrar_topico(request, plano_id):
    """Cadastra um novo tópico de aula"""

    plano = get_object_or_404(NovoPlano.objects.all().filter(pk=plano_id))
    quantidade_topicos = NovoTopicoAula.objects.all().filter(plano_curso_id=plano_id, professor_id=request.user.pk).count()
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
            novo_topico = NovoTopicoAula(professor_id=request.user.pk, plano_curso_id=plano_curso, titulo=titulo, descricao=descricao)
            novo_topico.save()
            messages.success(request, 'Tópico de aula cadastrado')
            return render(request, 'cursos/cadastrar_topico.html', contexto)
        elif plano.status == 'REPROVADO':
            messages.error(request, 'Plano RECUSADO, impossível cadastrar tópicos de aula.')
            return render(request, 'cursos/cadastrar_topico.html', contexto)
        else:
            messages.error(request, 'Quantidade máxima de tópicos excedida (MAX: 5 tópicos)')
            return render(request, 'cursos/cadastrar_topico.html', contexto)


def gera_certificado(request):
    cursos = NovoPlano.objects.filter(id_professor=request.user.pk, status='APROVADO').order_by('data_criacao')
    token_existe = TokenCertificado.objects.filter(professor_id=request.user.pk).exists()
    if not token_existe:
        token = secrets.token_hex(16)
        valida_token = TokenValidacao.objects.all().filter(token=token).exists()
        certificado_existe = TokenCertificado.objects.all().filter(professor_id=request.user.pk).exists()
        if valida_token:
            token = secrets.token_hex(16)

        if not certificado_existe:
            novo_token = TokenValidacao(token=token)
            novo_token.save()
            novo_certificado = TokenCertificado(professor_id=request.user.pk, token=token)
            novo_certificado.save()

    token = get_object_or_404(TokenCertificado.objects.filter(professor_id=request.user.pk))

    contexto = {
        'cursos': cursos,
        'token': token
    }

    return render(request, 'cursos/certificado.html', contexto)


def gera_pdf(request):
    pasta_app = os.path.dirname(__file__)
    cnv = canvas.Canvas(pasta_app+'\\certificado.pdf', pagesize=A4)
    cnv.getCurrentPageContent()
    cnv.save()
    return redirect('gera_certificado')


def valida_certificado(request):
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        token_enviado = request.POST['token']
        captcha_token = request.POST.get("g-recaptcha-response")
        captcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        captcha_secret = '6LfHUjghAAAAALAyVR0ia2muNZ6CC5wBLD5hHJ_F'
        captcha_data = {
            'secret': captcha_secret,
            'response': captcha_token
        }
        contexto = {
            'form': form
        }
        captcha_server_responde = requests.post(url=captcha_url, data=captcha_data)
        captcha_json = json.loads(captcha_server_responde.text)
        if captcha_json['success'] == False:
            messages.error(request, 'reCAPTCHA inválido')
            return render(request, 'cursos/validar_certificado.html', contexto)
        validacao = TokenValidacao.objects.all().filter(token=token_enviado).exists()
        if validacao:
            messages.success(request, 'Certificado válido')
        else:
            messages.error(request, 'Certificado inválido')
        return render(request, 'cursos/validar_certificado.html', contexto)

    else:
        contexto = {
            'form': CaptchaForm
        }
        return render(request, 'cursos/validar_certificado.html', contexto)
