# AVASUS-lais-backend
Repositório destinado ao armazenamento e versionamento do desafio/fase 2 da seleção para pesquisador no Projeto “PESQUISA APLICADA A IMPLEMENTAÇÃO DE PROCESSOS EDUCACIONAIS EM SISTEMAS INTEGRADOS DE INFORMAÇÃO E COMUNICAÇÃO EM SAÚDE”. Edital 021/2022 LAIS/HUOL/UFRN.

Candidato: Júlio César Almeida Soares

# Instalação
### Instalação de Ambiente Virtual
- Baixe esse repositório e Entre no diretório respectivo
- Utilize um VirtualEnvironment<br>
`python -m venv venv`


### Passos Iniciais para Funcionamento do Projeto
 - Crie e Execute de migrations para o banco de dados<br>
`python manage.py makemigrations`<br>
`python manage.py migrate`

- É necessário criar um SuperUsuário<br>
`python manage.py createsuperuser`
	- Dados necessários:
		- CPF Válido ( [Gerador de CPF](https://www.4devs.com.br/gerador_de_cpf) )
		- Data de Nascimento
		- Senha
    - Titulação (GRADUACAO, ESPECIALIZACAO, MESTRADO OU DOUTORADO)
    - Termos de uso (SIM ou NAO)

- Agora é so iniciar o servidor<br>
	`python .manage.py runserver

