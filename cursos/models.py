from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Avaliacao(models.TextChoices):
    AGUARDANDO_AVALIACAO = 'AGUARDANDO_AVALIACAO', _('Aguardando avaliação')
    APROVADO = 'APROVADO', _('Aprovado')
    REPROVADO = 'REPROVADO', _('Reprovado')


class AreaTematica(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


class NovoPlano(models.Model):
    class Meta:
        verbose_name_plural = 'Planos de curso'

    id_professor = models.IntegerField(verbose_name='Id do professor')
    professor_responsavel = models.CharField(verbose_name='Professor responsável', max_length=150)
    titulo = models.CharField(verbose_name='Título', max_length=120)
    area_tematica = models.ForeignKey(AreaTematica, verbose_name='Áreas temáticas', on_delete=models.CASCADE)
    carga_horaria = models.IntegerField(verbose_name='Carga horároia', validators=[MinValueValidator(3), MaxValueValidator(350)])
    ementa = models.CharField(verbose_name='Ementa', max_length=250)
    obj_geral = models.TextField(verbose_name='Objetivo geral', max_length=250)
    status = models.TextField(verbose_name='Status', choices=Avaliacao.choices, default=0)