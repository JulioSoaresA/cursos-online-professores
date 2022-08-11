from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from markdownx.models import MarkdownxField


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
    carga_horaria = models.IntegerField(verbose_name='Carga horária', validators=[MinValueValidator(3), MaxValueValidator(350)])
    ementa = models.CharField(verbose_name='Ementa', max_length=250)
    obj_geral = models.TextField(verbose_name='Objetivo geral', max_length=250)
    data_criacao = models.DateTimeField(verbose_name='Data de criação')
    status = models.TextField(verbose_name='Status', choices=Avaliacao.choices, default=0)

    def __str__(self):
        return self.titulo


class NovoTopicoAula(models.Model):
    class Meta:
        verbose_name = 'Tópicos de aula'

    plano_curso = models.ForeignKey(NovoPlano, on_delete=models.CASCADE, related_name='plano')
    professor_id = models.IntegerField()
    titulo = models.CharField(verbose_name='Título', max_length=120)
    descricao = MarkdownxField()

    def __str__(self):
        return self.titulo


class TokenValidacao(models.Model):
    token = models.TextField(verbose_name='Token', max_length=32)

    def __str__(self):
        return self.token


class TokenCertificado(models.Model):
    professor_id = models.IntegerField()
    token = models.TextField(verbose_name='Token', max_length=32)

    def __str__(self):
        return self.token
