from django.urls import path
from . import views

urlpatterns = [
    path('plano_de_curso/', views.plano_de_curso, name='plano_de_curso'),
    
]
