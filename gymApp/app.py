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
def add_aluno():
    if request.method == 'GET':
        
        try:
            cursor.execute('select codigo, nome, valor from plano')
            plano = cursor.fetchall()

            cursor.execute('select turma_cod, modalidade_nome, modalidade_faixa_etaria from turma_modalidade')
            turma = cursor.fetchall()
        except:
            session['msg'] = 'Erro ao carregar dados'
            return redirect('/')
        
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
        
        
        image_url=''
        if aluno[3] != None and aluno[3] != '':
            # gera um nome temporario aleatorio para a imagem
            image_url = f'static/images/{uuid.uuid4()}.jpeg'

            # salva a imagem temporariamente em /static/images
            f = io.BytesIO(aluno[3])
            data = f.read()
            d = open(image_url, 'wb')
            d.write(data)
            d.close()
        
        try:
            cursor.execute(f"select fk_turma_codigo, fk_aluno_cpf from esta_matriculado where fk_aluno_cpf='{cpf}'")
            aluno_turma = cursor.fetchall()[0]
        except: 
            aluno_turma = ''
        
        cursor.execute('select codigo, nome, valor from plano')
        plano = cursor.fetchall()

        try:
            cursor.execute('select turma_cod, modalidade_nome, modalidade_faixa_etaria from turma_modalidade')
            turma = cursor.fetchall()
        except:
            turma = ''
        
        return render_template('edit_aluno.html', plano=plano, turma=turma, aluno=aluno, aluno_turma=aluno_turma, image_url=image_url)

    elif request.method == 'POST':

        # remove a imagem temporaria
        image_url = request.args.get('img')
        if image_url:
            os.remove(ABS_PATH+image_url)

        # dados do formulario
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        foto = request.files['foto'].stream.read()
        fk_plano_codigo = request.form.get('fk_plano_codigo')
        fk_turma = request.form.get('fk_turma')

        print('$$$$$', cpf)

        try:
            if foto == b'':
                cursor.execute(f"update aluno set nome='{nome}', data_nascimento='{data_nascimento}', fk_plano_codigo='{fk_plano_codigo}' where cpf='{cpf}'")
            else:
                cursor.execute(f"update aluno set nome='{nome}', data_nascimento='{data_nascimento}', fk_plano_codigo='{fk_plano_codigo}', foto={Binary(foto)} where cpf='{cpf}'")

            cursor.execute(f"select * from esta_matriculado where fk_aluno_cpf='{cpf}'")
            if len(cursor.fetchall()) == 0:
                cursor.execute("insert into esta_matriculado values(%s, %s);", (fk_turma, cpf))
                conexao.commit()
            else:
                cursor.execute(f"update esta_matriculado set fk_turma_codigo={fk_turma} where fk_aluno_cpf='{cpf}' ")
                conexao.commit()
        
            session['messages'] = 'Aluno editado com sucesso'
        except:
            session['messages'] = 'Erro ao editar aluno'

        return redirect('/')

@app.route('/delete_aluno', methods=['POST'])
def delete_aluno():

    if request.method == 'POST':
        cpf = request.form.get('aluno')

        try:
            cursor.execute(f"delete from esta_matriculado where fk_aluno_cpf='{cpf}'")
            cursor.execute(f"delete from aluno where cpf='{cpf}'")
            conexao.commit()
        except:
            session['messages'] = 'Erro ao deletar aluno'
            return redirect('/')

        session['messages'] = 'Aluno deletado com sucesso'
        return redirect('/')

@app.route('/add_turma', methods=['GET', 'POST'])
def add_turma():
    if request.method == 'GET':

        try:
            cursor.execute('select codigo, nome, faixa_etaria from modalidade')
            modalidade = cursor.fetchall()

            cursor.execute('select cpf, nome from profissional')
            profissional = cursor.fetchall()

            cursor.execute('select codigo, numero, endereco from sala_unidade')
            sala = cursor.fetchall()
        except:
            session['messages'] = 'Erro ao carregar dados'
            return redirect('/')
        
        return render_template('add_turma.html', modalidade=modalidade, profissional=profissional, sala=sala)

    elif request.method == 'POST':

        # pega dados do formulario
        modalidade = request.form.get('fk_modalidade_codigo')
        profissional = request.form.get('fk_profissional_cpf')
        sala = request.form.get('fk_sala_codigo')
        horario_inicio = request.form.get('horario_inicio')
        horario_fim = request.form.get('horario_fim')
        dia_semana = request.form.get('dia_semana')


        try:
            cursor.execute("call criar_turma(%s, %s, %s, %s, %s, %s);", (modalidade, profissional, sala, horario_inicio, horario_fim, dia_semana))
            conexao.commit()
        
        except:
            session['messages'] = 'Erro ao inserir turma'
            return redirect('/')
        
        
        session['messages'] = 'Turma adicionada com sucesso'
        return redirect('/')

    
@app.route('/edit_turma', methods=['GET', 'POST'])
def edit_turma():
    if request.method == 'GET':

        try:
            turma_cod = request.args.get('turma')

            cursor.execute(f'select fk_modalidade_codigo, fk_sala_codigo, fk_profissional_cpf, horario_inicio, horario_fim, dia_semana from turma_mod_sala where codigo = {turma_cod}')
            mod_cod, sala_cod, pro_cod, horario_inicio, horario_fim, dia_semana = cursor.fetchall()[0]

            cursor.execute(f'select codigo, nome, faixa_etaria from modalidade')
            modalidades = cursor.fetchall()

            cursor.execute('select cpf, nome from profissional')
            profissionais = cursor.fetchall()

            cursor.execute('select codigo, numero, endereco from sala_unidade')
            salas = cursor.fetchall()

            cursor.execute('select codigo, numero, endereco from sala_unidade')
            salas = cursor.fetchall()
        
        except:
            session['messages'] = 'Erro ao carregar dados'
            return redirect('/')
        
        return render_template('edit_turma.html', modalidade=modalidades, mod_cod=mod_cod, profissional=profissionais, pro_cod=pro_cod, sala=salas, sala_cod=sala_cod, horario_inicio=horario_inicio, horario_fim=horario_fim, dia_semana=dia_semana, turma_cod=turma_cod)

    elif request.method == 'POST':

        try:
            # pega dados do formulario
            turma_cod = request.form.get('turma_cod')
            modalidade = request.form.get('fk_modalidade_codigo')
            profissional = request.form.get('fk_profissional_cpf')
            sala = request.form.get('fk_sala_codigo')
            horario_inicio = request.form.get('horario_inicio')
            horario_fim = request.form.get('horario_fim')
            dia_semana = request.form.get('dia_semana')

            # updates
            cursor.execute(f"update turma set fk_modalidade_codigo={modalidade} where codigo={turma_cod}")
            cursor.execute(f"update conduz set fk_profissional_cpf='{profissional}' where fk_turma_codigo={turma_cod}")
            cursor.execute(f"update utiliza set fk_sala_codigo={sala}, horario_inicio='{horario_inicio}', horario_fim='{horario_fim}', dia_semana='{dia_semana}' where fk_turma_codigo={turma_cod}")

            conexao.commit()

        except:
            session['messages'] = 'Erro ao inserir turma'
            return redirect('/')
        
        session['messages'] = 'Turma editada com sucesso'
        return redirect('/')


@app.route('/del_turma', methods=['POST'])
def del_turma():
    if request.method == 'POST':

        try:
            turma_cod = request.form.get('turma_cod')

            # delete
            cursor.execute(f"delete from utiliza where fk_turma_codigo={turma_cod}")
            cursor.execute(f"delete from conduz where fk_turma_codigo={turma_cod}")
            cursor.execute(f"delete from esta_matriculado where fk_turma_codigo={turma_cod}")
            cursor.execute(f"delete from turma where codigo={turma_cod}")
            conexao.commit()

        except:
            session['messages'] = 'Erro ao remover turma'
            return redirect('/')
    
        session['messages'] = 'Turma removida com sucesso'
        return redirect('/')

@app.route('/modalidade', methods=['GET', 'POST'])
def modalidade():
    if request.method == 'GET':
        return render_template('modalidade.html')
        
    elif request.method == 'POST':

        try:
            nome = request.form.get('nome')
            faixa_etaria = request.form.get('faixa_etaria')

            cursor.execute("insert into modalidade(nome, faixa_etaria) values(%s,%s)", (nome, faixa_etaria))
            conexao.commit()

        except:
            session['messages'] = 'Erro ao inserir modalidade'
            return redirect('/')

        session['messages'] = 'Modalidade criada com sucesso'
        return redirect('/')

@app.route('/edit_modalidade', methods=['GET', 'POST'])
def edit_modalidade():
    if request.method == 'GET':

        try:
            mod_nome = request.args.get('mod')

            cursor.execute(f"select codigo, nome, faixa_etaria from modalidade where nome='{mod_nome}'")

            modalidade = cursor.fetchall()[0]

        except:
            session['messages'] = 'Erro ao carregar dados'
            return redirect('/')

        return render_template('modalidade.html', modalidade=modalidade)

    elif request.method == 'POST':

        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        faixa_etaria = request.form.get('faixa_etaria')

        cursor.execute(f"UPDATE modalidade SET nome='{nome}', faixa_etaria='{faixa_etaria}' where codigo={codigo} ")
        conexao.commit()

        return redirect('/')

@app.route('/del_modalidade', methods=['POST'])
def del_modalidade():
    if request.method == 'POST':

        mod_cod = request.form.get('codigo')

        # delete
        try:
            cursor.execute(f"delete from esta_matriculado where fk_turma_codigo in (select codigo from turma where fk_modalidade_codigo = {mod_cod})")
            cursor.execute(f"delete from utiliza where fk_turma_codigo in (select codigo from turma where fk_modalidade_codigo = {mod_cod})")
            cursor.execute(f"delete from turma where fk_modalidade_codigo = {mod_cod}")
            cursor.execute(f"delete from modalidade where codigo = {mod_cod}")

            conexao.commit()

        except:
            session['messages'] = 'Erro ao remover modalidade'
            return redirect('/')
    
        session['messages'] = 'Modalidade removida com sucesso'
        return redirect('/')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')
