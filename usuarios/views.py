from django.shortcuts import render
from django.contrib import auth, messages
from .models import Usuario
from usuarios.forms import Autocadastro


def autocadastro(request):
    """Cadastra uma nova pessoa no sustema"""

    if request.method == 'GET':
        form = Autocadastro()
        contexto = {'form': form}
        return render(request, 'usuarios/autocadastro.html', contexto)
    else:
        form = Autocadastro(request.POST)
        if form.is_valid():
            form = Autocadastro()
            contexto = {'form': form}
            nome_completo = request.POST['nome_completo']
            cpf = request.POST['cpf']
            data_nascimento = request.POST['data_nascimento']
            titulacao = request.POST['titulacao']
            termos_de_uso = request.POST['termos_de_uso']
            senha = request.POST['password']
            user = Usuario.objects.create_user(cpf=cpf, nome_completo=nome_completo, data_nascimento=data_nascimento, titulacao=titulacao, termos_de_uso=termos_de_uso, password=senha)
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso')
            return render(request, 'usuarios/autocadastro.html', contexto)
        else:
            contexto = {'form': form}
            return render(request, 'usuarios/autocadastro.html', contexto)


def login(request):
    return render(request, 'usuarios/login.html')


def dashboard(request):
    return render(request, 'usuarios/dashboard.html')


def logout(request):
    return None