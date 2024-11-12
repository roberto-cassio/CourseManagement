# Projeto para Gerenciamento de Cursos Online
**Descrição**: Este projeto é um sistema de gerenciamento de cursos online, desenvolvido em Django e Django REST Framework, que permite o gerenciamento de professores, cursos, aulas e matrículas de estudantes. O sistema oferece operações CRUD (Create, Read, Update e Delete) para cada entidade, além de uma funcionalidade de deleção lógica para manter o histórico de alunos, cursos, matrículas e aulas anteriores. Ele utiliza autenticação baseada em token JWT e fornece endpoints organizados para facilitar a integração com aplicações frontend.

## Pré Requisitos:
- Python (>= 3.8)
- Django (>= 3.2)
- Banco de Dados: MSSQL
- Driver ODBC para SQL Server (necessário para a conexão com o banco de dados MSSQL): <br>
Windows:Pode ser instalado a partir do [link oficial da Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16). <br>
Linux: Instale o driver usando o seguinte comando (para distribuições baseadas em Debian, como Ubuntu):
```
bash
Copiar código
sudo apt-get install msodbcsql17
```
## Instalação:
### Clone o Repositório:
```
git clone https://github.com/roberto-cassio/CourseManagement
cd CourseManagement
```
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
SECRET_KEY = 'sua_chave_secreta'
NAME =  'nome_do_banco'
USER= 'usuario_do_banco'
PASSWORD= 'senha_do_banco'
HOST='localhost'
```

- Para obtenção de uma nova SECRET_KEY:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- Basta preencher o campo correspondente com a chave obtida.
### Aplique as Migrações no seu banco:
```
python manage.py makemigrations
python manage.py migrate
```

### Caso deseje popular o banco de dados:
```
python manage.py loaddata initial_data.json
```

## Configuração:
Conforme instruído na seção de Instalação, a configuração necessária envolve o arquivo .env, com informações para configuração do banco de dados e chaves de autenticação.
1. Para acesso aos end_points, é necessário possuir um Token JWT. Para tal será necessário: <br>
Utilizar o comando createsuperuser para criar um usuário:
```
python manage.py createsuperuser
```


## Uso:
1. Para inicializar a aplicação:
```
python manage.py runserver
```
2. Acesso pode ser realizado no navegador através do http://127.0.0.1:8000/ - Para mais informações End-Points acesse a documentação
3. Para acesso aos End-Points é necessário um Token JWT, com o usuário criado anteriormente com o JWT faça uma requisição **POST** em
http://127.0.0.1:8000/token com o corpo da requisição no formato:
```
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
- Isso retornará um Token JWT necessário para demais requisições da API.
3.1 - Acesso também pode ser realizado através do "Authorization no Swagger" - http://127.0.0.1:8000/swagger

## Testes:
A aplicação inclui Test Cases para suas principais funcionalidades, os mesmos pode ser executados em:
```
pytest -s coursemanagement/tests/
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
3. É valido lembrar que os tokens JWT expiram periodicamente, sendo necessário atualiza-los regularmente. Dentro do Swagger, para realizar a Autorização pelo JWT basta acessar o botão **Authorize** no canto superior direito. Na tela aberta será necessário preencher com sua chave JWT no formato:
```
"Bearer sua_chave_aqui"
```
