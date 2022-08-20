from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from usuarios.models import Usuario
from cursos.forms.planoCursoForm import NovoPlanoForm
from cursos.forms.topicoForm import NovoTopicoForm
from .models import NovoPlano, NovoTopicoAula, TokenValidacao, TokenCertificado
from cursos.forms.captchaForm import CaptchaForm
from datetime import datetime
import secrets
import json
import requests
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def plano_de_curso(request):

    """Cadastra um novo plano de curso"""
    form = NovoPlanoForm(request.POST)

    if form.is_valid():

        titulo = request.POST['titulo']
        area_tematica = request.POST['area_tematica']
        carga_horaria = request.POST['carga_horaria']
        ementa = request.POST['ementa']
        obj_geral = request.POST['obj_geral']
        if NovoPlano.objects.all().filter(titulo=titulo).exists():
            messages.error(request, 'Este título já existe')
            return redirect('index')
        id_professor = request.user.pk
        professor_responsavel = request.user.nome_completo
        novo_plano = NovoPlano.objects.create(id_professor=id_professor,
                                              professor_responsavel=professor_responsavel, titulo=titulo,
                                              area_tematica_id=area_tematica, carga_horaria=carga_horaria,
                                              ementa=ementa, obj_geral=obj_geral, status='AGUARDANDO_AVALIACAO',
                                              data_criacao=datetime.now())
        novo_plano.save()
        messages.success(request, 'Novo plano cadastrado com sucesso')
        return redirect('index')
    else:
        carga_horaria = int(request.POST['carga_horaria'])
        if carga_horaria < 3 or carga_horaria > 350:
            messages.error(request, 'Carga horária fora do limite permitido')
            return redirect('index')
        else:
            messages.error(request, 'Porfavor, preencha todos os campos.')
            return redirect('index')


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
        form = NovoTopicoForm()

        contexto = {
            'form': form,
            'plano': plano
        }
        if plano.status == 'REPROVADO':
            messages.error(request, 'Plano RECUSADO, impossível cadastrar tópicos de aula.')
        return render(request, 'cursos/cadastrar_topico.html', contexto)
    else:
        form = NovoTopicoForm()

        contexto = {
            'form': form,
            'plano': plano
        }
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        plano_curso = request.POST.get('plano_curso')

        if quantidade_topicos < 5 and plano.status == 'APROVADO' and not NovoTopicoAula.objects.all().filter(titulo=titulo).exists():
            novo_topico = NovoTopicoAula(professor_id=request.user.pk, plano_curso_id=plano_curso, titulo=titulo, descricao=descricao)
            novo_topico.save()
            messages.success(request, 'Tópico de aula cadastrado')
            return render(request, 'cursos/cadastrar_topico.html', contexto)
        elif plano.status == 'REPROVADO':
            messages.error(request, 'Plano RECUSADO, impossível cadastrar tópicos de aula.')
            return render(request, 'cursos/cadastrar_topico.html', contexto)
        elif NovoTopicoAula.objects.all().filter(titulo=titulo).exists():
            messages.error(request, 'Titulo já existente.')
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
    user = get_object_or_404(Usuario.objects.filter(pk=request.user.pk))
    cursos = NovoPlano.objects.filter(id_professor=request.user.pk, status='APROVADO').order_by('data_criacao')
    token = get_object_or_404(TokenCertificado.objects.filter(professor_id=request.user.pk))

    template_path = 'cursos/pdf.html'
    context = {'cursos': cursos,
               'user': user,
               'token': token
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="certificado.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


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
