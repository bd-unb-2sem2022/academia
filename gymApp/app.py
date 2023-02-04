from flask import Flask, render_template, request, redirect, session
from psycopg2 import Binary
from db import conexao

app = Flask(__name__)

app.secret_key = 'e7b047ff4089f5d0a187d4c44d8633115af223407bd578511c3ba346cf860805'
app.config['SESSION_TYPE'] = 'filesystem'

cursor = conexao.cursor()

# routes
@app.route('/')
def index():
    try:
        messages = session['messages']
    except:
        messages = ''

    cursor.execute('select aluno, turma_codigo, modalidade, unidade_nome, cpf from nome_aluno_modalidade_unidade')
    res = cursor.fetchall()
    return render_template('index.html', alunos=res, messages=messages)

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
            cursor.execute("insert into esta_matriculado values (%s,%s)", (fk_turma, cpf))
            conexao.commit()
            
            session['messages'] = 'Aluno inserido com sucesso'
        except:
            session['messages'] = 'Erro ao inserir aluno'

        return redirect('/')

    else:
        session['messages'] = 'verbo HTTP não permitido'
        return redirect('/')

@app.route('/delete_aluno')
def delete_aluno():
    cpf = request.args.get('aluno')

    try:
        cursor.execute(f"delete from esta_matriculado where fk_aluno_cpf='{cpf}'")
        cursor.execute(f"delete from aluno where cpf='{cpf}'")
        conexao.commit()
    except:
        session['messages'] = 'Erro ao deletar aluno'
        return redirect('/')

    session['messages'] = 'Aluno deletado com sucesso'
    return redirect('/')
    
@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')
