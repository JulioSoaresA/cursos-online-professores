from datetime import datetime, date
from validate_docbr import CPF
from usuarios.models import Usuario


def senhas_diferentes(senha, senha2, lista_de_erros):
    """Verifica se a senha e confirmação de senha são diferentes"""

    if senha != senha2:
        lista_de_erros['password2'] = 'As senhas estão diferentes'


def data_valida(data_nascimento, lista_de_erros):
    """Verifica se a data é válida"""

    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    if idade < 18:
        lista_de_erros['data_nascimento'] = 'Menores de idade não são permitidos'


def cpf_valido(cpf_recebido, lista_de_erros):
    """Verifica se o CPF é válido"""

    cpf_base = CPF()
    if not cpf_base.validate(cpf_recebido):
        lista_de_erros['cpf'] = 'CPF inválido'


def cpf_existente(cpf_recebido, lista_de_erros):
    """Verifica se o CPF já está cadastrado"""

    existe = Usuario.objects.filter(cpf=cpf_recebido).exists()
    if existe:
        lista_de_erros['cpf'] = 'CPF já cadastrado'


def termo_de_uso_valido(termos_de_uso, lista_de_erros):
    """Verifica os termos de uso"""

    if termos_de_uso == 'NAO':
        lista_de_erros['termos_de_uso'] = 'Os termos de uso devem ser aceitos'
