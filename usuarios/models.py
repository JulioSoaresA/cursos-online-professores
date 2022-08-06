from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date


class Titulacao(models.TextChoices):
    GRADUACAO = 'GRADUACAO', _('Graduação')
    ESPECIALIZACAO = 'ESPECIALIZACAO', _('Especialização')
    MESTRADO = 'MESTRADO', _('Mestrado')
    DOUTORADO = 'DOUTORADO', _('Doutorado')


class TermosDeUso(models.TextChoices):
    SIM = 'SIM', _('Sim')
    NAO = 'NAO', _('Não')


class GerenciadorUsuarios(BaseUserManager):
    def create_user(self, cpf, nome_completo, data_nascimento, titulacao, termos_de_uso, password=None):
        if not cpf:
            raise ValueError('Usuarios davem possuir um cpf')
        if not nome_completo:
            raise ValueError('Usuarios davem possuir um nome')
        if not data_nascimento:
            raise ValueError('Usuarios davem possuir uma data de nascimento')

        user = self.model(
            cpf=cpf,
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            titulacao=titulacao,
            termos_de_uso=termos_de_uso,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, nome_completo, data_nascimento, titulacao, termos_de_uso, password):
        user = self.create_user(
            cpf=cpf,
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            titulacao=titulacao,
            termos_de_uso=termos_de_uso,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    class Meta:
        verbose_name_plural = 'Usuários'

    email = models.EmailField(verbose_name='email', max_length=255)
    username = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    nome_completo = models.CharField(verbose_name='Nome completo', max_length=100)
    cpf = models.CharField(verbose_name='CPF', max_length=11, unique=True)
    data_nascimento = models.DateField(verbose_name='Data de nascimento')
    titulacao = models.TextField(verbose_name='Titulação', choices=Titulacao.choices, default=0)
    termos_de_uso = models.TextField(verbose_name='Termos de uso', choices=TermosDeUso.choices, max_length=3, default=0)
    password2 = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome_completo', 'data_nascimento', 'termos_de_uso', 'titulacao']

    objects = GerenciadorUsuarios()

    def get_idade(self):
        if self.data_nascimento:
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))

    def __str__(self):
        return self.nome_completo

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
