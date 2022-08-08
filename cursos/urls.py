from django.urls import path
from . import views

urlpatterns = [
    path('plano_de_curso/', views.plano_de_curso, name='plano_de_curso'),
    path('info_curso/<int:plano_id>', views.info_curso, name='info_curso'),
    
]
