from django.shortcuts import render
from cursos.models import NovoPlano, AreaTematica
from django.core.paginator import Paginator


def index(request):
    if request.user.is_authenticated:
        id_professor = request.user.pk
        planos = NovoPlano.objects.order_by('data_criacao').filter(id_professor=id_professor)
        paginator = Paginator(planos, 3)
        pag = request.GET.get('page')
        planos_por_pag = paginator.get_page(pag)
        quantidade_cursos_aprovados = NovoPlano.objects.filter(id_professor=request.user.pk, status='APROVADO').count()
        areas_tematicas = AreaTematica.objects.all()

        contexto = {
            'planos': planos_por_pag,
            'quantidade_cursos_aprovados': quantidade_cursos_aprovados,
            'areas_tematicas': areas_tematicas
        }
        return render(request, 'professores/index.html', contexto)
    else:
        return render(request, 'professores/index.html')
