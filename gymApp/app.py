from flask import Flask, render_template, request, redirect
from psycopg2 import Binary
from db import conexao

app = Flask(__name__)

cursor = conexao.cursor()

# routes
@app.route('/')
def index():
    cursor.execute('select aluno, turma_codigo, modalidade, unidade_nome from nome_aluno_modalidade_unidade')
    res = cursor.fetchall()
    return render_template('index.html', alunos=res)

@app.route('/add_aluno', methods=['GET', 'POST'])
def get_add_aluno():
    if request.method == 'GET':
        
        cursor.execute('select codigo, nome, valor from plano')
        plano = cursor.fetchall()

        cursor.execute('select codigo, fk_modalidade_codigo from turma')
        turma = cursor.fetchall()
        
        return render_template('add_aluno.html', plano=plano, turma=turma)

    elif request.method == 'POST':

        # dados do formulario
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        foto = Binary(request.files['foto'].stream.read())
        fk_plano_codigo = request.form.get('fk_plano_codigo')
        fk_turma = request.form.get('fk_turma')

        # TODO: validação e sanitização dos dados inseridos


        try:
            cursor.execute("insert into aluno values (%s,%s,%s,%s,%s)", (cpf, nome, data_nascimento, foto, fk_plano_codigo))
            conexao.commit()

            cursor.execute(f"insert into esta_matriculado values ('{fk_turma}', '{cpf}')")
            conexao.commit()
        except:
            return 'Erro ao inserir aluno'

        return redirect('/')

    else:
        return redirect('/')

