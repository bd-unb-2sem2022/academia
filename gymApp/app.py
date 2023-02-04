from flask import Flask, render_template, request, redirect, session
from psycopg2 import Binary
from db import conexao
import io, uuid, os


app = Flask(__name__)
app.secret_key = 'e7b047ff4089f5d0a187d4c44d8633115af223407bd578511c3ba346cf860805'
app.config['SESSION_TYPE'] = 'filesystem'

ABS_PATH = os.path.abspath(__file__)[:-6]

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

@app.route('/edit_aluno', methods=['GET', 'POST'])
def edit_aluno():
    cpf = request.args.get('aluno')

    if request.method == 'GET':

        try:
            cursor.execute(f"select cpf, nome, data_nascimento, foto, fk_plano_codigo from aluno where cpf='{cpf}'")
            aluno = cursor.fetchall()[0]
        except:
            session['message'] = 'Usuario não encontrado'
            return redirect('/')
        
        # gera um nome temporario aleatorio para a imagem
        image_url = f'static/images/{uuid.uuid4()}.jpeg'

        # salva a imagem temporariamente em /static/images
        f = io.BytesIO(aluno[3])
        data = f.read()
        d = open(image_url, 'wb')
        d.write(data)
        d.close()
        
        cursor.execute(f"select fk_turma_codigo, fk_aluno_cpf from esta_matriculado where fk_aluno_cpf='{cpf}'")
        aluno_turma = cursor.fetchall()[0]
        
        cursor.execute('select codigo, nome, valor from plano')
        plano = cursor.fetchall()

        cursor.execute('select codigo, fk_modalidade_codigo from turma')
        turma = cursor.fetchall()
        
        return render_template('edit_aluno.html', plano=plano, turma=turma, aluno=aluno, aluno_turma=aluno_turma, image_url=image_url)

    elif request.method == 'POST':

        # remove a imagem temporaria
        image_url = request.args.get('img')
        os.remove(ABS_PATH+image_url)

        # dados do formulario
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        foto = request.files['foto'].stream.read()
        fk_plano_codigo = request.form.get('fk_plano_codigo')
        fk_turma = request.form.get('fk_turma')

        try:
            if foto == b'':
                cursor.execute(f"update aluno set nome='{nome}', data_nascimento='{data_nascimento}', fk_plano_codigo='{fk_plano_codigo}' where cpf='{cpf}'")
            else:
                cursor.execute(f"update aluno set nome='{nome}', data_nascimento='{data_nascimento}', fk_plano_codigo='{fk_plano_codigo}', foto={Binary(foto)} where cpf='{cpf}'")

            cursor.execute(f"update esta_matriculado set fk_turma_codigo={fk_turma} where fk_aluno_cpf='{cpf}' ")
            conexao.commit()
        
            session['messages'] = 'Aluno editado com sucesso'
        except:
            session['messages'] = 'Erro ao editar aluno'

        return redirect('/')
    
@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')
