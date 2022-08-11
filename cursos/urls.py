from django.urls import path
from . import views

urlpatterns = [
    path('plano_de_curso/', views.plano_de_curso, name='plano_de_curso'),
    path('info_curso/<int:plano_id>', views.info_curso, name='info_curso'),
    path('cadastrar_topico/<int:plano_id>', views.cadastrar_topico, name='cadastrar_topico'),
    path('certificado/', views.gera_certificado, name='gera_certificado'),
    path('gera_pdf/', views.gera_pdf, name='gera_pdf'),
    path('valida_certificado/', views.valida_certificado, name='valida_certificado')
]
