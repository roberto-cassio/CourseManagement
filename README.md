# Projeto para Gerenciamento de Cursos Online
**Descrição**: Este projeto é um sistema de gerenciamento de cursos online, desenvolvido em Django e Django REST Framework, que permite o gerenciamento de professores, cursos, aulas e matrículas de estudantes. O sistema oferece operações CRUD (Create, Read, Update e Delete) para cada entidade, além de uma funcionalidade de deleção lógica para manter o histórico de alunos, cursos, matrículas e aulas anteriores. Ele utiliza autenticação baseada em token JWT e fornece endpoints organizados para facilitar a integração com aplicações frontend.

## Pré Requisitos:
- Python (>= 3.8)
- Django (>= 3.2)
- Banco de Dados: MSSQL

## Instalação:
### Clone o Repositório:
git clone https://github.com/roberto-cassio/CourseManagement
cd CourseManagement

### Crie e ative o Ambiente Virtual:
```
-Linux:
python3 -m venv venv
source venv/bin/activate
-Windows:
python -m venv venv
venv\Scripts\activate
```

### Baixe as Dependências do Projeto:
```
pip install -r requirements.txt
```

### Configurar Variáveis de Ambiente: 
Crie um arquivo .env baseado no exemplo abaixo para configuração do banco de dados e outras varíaveis importantes:
```
SECRET_KEY='sua_chave_secreta'
DEBUG=True
DB_NAME='nome_do_banco'
DB_USER='usuario_do_banco'
DB_PASSWORD='senha_do_banco'
DB_HOST='localhost'
```
### Aplique as Migrações no seu banco:
```
python manage.py migrate
```

## Configuração:
Conforme instruído na seção de Instalação, a configuração necessária envolve o arquivo .env, com informações para configuração do banco de dados e chaves de autenticação.

## Uso:
1. Para inicializar a aplicação:
```
python manage.py runserver
```
2. Acesso pode ser realizado no navegador através do http://127.0.0.1:8000

## Testes:
A aplicação inclui Test Cases para suas principais funcionalidades, os mesmos pode ser rodados em:
```
python manage.py test coursemanagement/tests/
```
## Documentação:
Toda a aplicação se encontra documentada através do Swagger, a mesma pode ser visualizada da seguinte forma:
1. Inicie a aplicação com
```
python manage.py runserver
```
2. Acesse o seguinte end_point:
```
http://127.0.0.1:8000/swagger
```
