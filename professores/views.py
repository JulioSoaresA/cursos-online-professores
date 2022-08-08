from django.shortcuts import render
from cursos.models import NovoPlano


def index(request):
    if request.user.is_authenticated:
        id_professor = request.user.pk
        planos = NovoPlano.objects.filter(id_professor=id_professor)
        contexto = {'planos': planos}
        return render(request, 'professores/index.html', contexto)
    else:
        return render(request, 'professores/index.html')
