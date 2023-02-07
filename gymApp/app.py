from flask import Flask, render_template, request, redirect, session
from psycopg2 import Binary
import io, uuid, os
import db, valid


app = Flask(__name__)
app.secret_key = 'e7b047ff4089f5d0a187d4c44d8633115af223407bd578511c3ba346cf860805'
app.config['SESSION_TYPE'] = 'filesystem'

ABS_PATH = os.path.abspath(__file__)[:-6]

# routes
@app.route('/')
def index():
    try:
        messages = session['messages']
    except:
        messages = ''

    res = db.query(['select aluno, turma_codigo, modalidade, unidade_nome, cpf from nome_aluno_modalidade_unidade'])[0]

    return render_template('index.html', alunos=res, messages=messages)

@app.route('/add_aluno', methods=['GET', 'POST'])
def add_aluno():
    if request.method == 'GET':
        
        try:
            plano, turma = db.query([
                'select codigo, nome, valor from plano',
                'select turma_cod, modalidade_nome, modalidade_faixa_etaria from turma_modalidade'
            ])
        except:
            session['messgages'] = 'Erro ao carregar dados'
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

        # valida dados
        if not (valid.valid_cpf(cpf) and valid.valid_nome(nome) and fk_plano_codigo != '' and data_nascimento != ''):
            session['messages'] = 'Dados inválidos'
            return redirect('/')

        try:

            db.query([
                "insert into aluno values ('%s','%s','%s',%s,'%s')" % (cpf, nome, data_nascimento, foto, fk_plano_codigo),
                "insert into esta_matriculado values ('%s','%s')" % (fk_turma, cpf)
            ])
            session['messages'] = 'Aluno inserido com sucesso'
        except:
            session['messages'] = 'Erro ao inserir aluno'

        return redirect('/')

@app.route('/edit_aluno', methods=['GET', 'POST'])
def edit_aluno():
    cpf = request.args.get('aluno')

    if request.method == 'GET':

        try:
            aluno = db.query([f"select cpf, nome, data_nascimento, foto, fk_plano_codigo from aluno where cpf='{cpf}'"])[0][0]
        except:
            session['messages'] = 'Usuario não encontrado'
            return redirect('/')
        
        
        image_url=''
        if aluno[3] != None and aluno[3] != '':
            # gera um nome temporario aleatorio para a imagem
            image_url = f'static/images/{uuid.uuid4()}.jpeg'

            # salva a imagem temporariamente em /static/images
            f = io.BytesIO(aluno[3])
            data = f.read()
            d = open(ABS_PATH+image_url, 'wb')
            d.write(data)
            d.close()
        
        aluno_turma = ''
        turma = ''
        try:
            aluno_turma, turma, plano = db.query([
                f"select fk_turma_codigo, fk_aluno_cpf from esta_matriculado where fk_aluno_cpf='{cpf}'",
                'select turma_cod, modalidade_nome, modalidade_faixa_etaria from turma_modalidade',
                'select codigo, nome, valor from plano'
            ])
            if len(aluno_turma) == 0:
                aluno_turma = ''
            else:
                aluno_turma = aluno_turma[0]

        except:
            session['messages'] = 'Erro ao carregar dados'
            return redirect('/')
        
        return render_template('edit_aluno.html', plano=plano, turma=turma, aluno=aluno, aluno_turma=aluno_turma, image_url=image_url)

    elif request.method == 'POST':

        # remove a imagem temporaria
        image_url = request.form.get('image_url')
        if image_url:
            os.remove(ABS_PATH+image_url)

        # dados do formulario
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        foto = request.files['foto'].stream.read()
        fk_plano_codigo = request.form.get('fk_plano_codigo')
        fk_turma = request.form.get('fk_turma')

        # valida dados
        if not (valid.valid_cpf(cpf) and valid.valid_nome(nome) and valid.valid_cod(fk_plano_codigo) and data_nascimento != ''):
            session['messages'] = 'Dados inválidos'
            return redirect('/')

        try:
            if foto == b'':
                db.query([f"update aluno set nome='{nome}', data_nascimento='{data_nascimento}', fk_plano_codigo='{fk_plano_codigo}' where cpf='{cpf}'"])
            else:
                db.query([f"update aluno set nome='{nome}', data_nascimento='{data_nascimento}', fk_plano_codigo='{fk_plano_codigo}', foto={Binary(foto)} where cpf='{cpf}'"])

            if fk_turma == '':
                try:
                    db.query([f"delete from esta_matriculado where fk_aluno_cpf='{cpf}'"])
                except:
                    pass
            else:
                res = db.query([f"select * from esta_matriculado where fk_aluno_cpf='{cpf}'"])[0]
                if len(res) == 0:
                    db.query(["insert into esta_matriculado values(%s, '%s') " % (fk_turma, cpf)])
                else:
                    db.query([f"update esta_matriculado set fk_turma_codigo={fk_turma} where fk_aluno_cpf='{cpf}' "])
        
            session['messages'] = 'Aluno editado com sucesso'
        except:
            session['messages'] = 'Erro ao editar aluno'

        return redirect('/')

@app.route('/delete_aluno', methods=['POST'])
def delete_aluno():

    if request.method == 'POST':
        cpf = request.form.get('aluno')

        try:
            db.query([
                f"delete from esta_matriculado where fk_aluno_cpf='{cpf}'",
                f"delete from aluno where cpf='{cpf}'"
            ])
        except:
            session['messages'] = 'Erro ao deletar aluno'
            return redirect('/')

        session['messages'] = 'Aluno deletado com sucesso'
        return redirect('/')

@app.route('/add_turma', methods=['GET', 'POST'])
def add_turma():
    if request.method == 'GET':

        try:
            modalidade, profissional, sala = db.query([
                'select codigo, nome, faixa_etaria from modalidade',
                'select cpf, nome from profissional',
                'select codigo, numero, endereco from sala_unidade'
            ])
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

        # valida dados
        if not (valid.valid_cod(modalidade) and valid.valid_cod(profissional) and valid.valid_cod(sala) and horario_inicio != '' and horario_fim != '' and dia_semana != ''):
            session['messages'] = 'Dados inválidos'
            return redirect('/')

        try:
            db.query(["call criar_turma(%s, '%s', %s, '%s', '%s', '%s');" % (modalidade, profissional, sala, horario_inicio, horario_fim, dia_semana)])
        
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

            data, modalidades, profissionais, salas = db.query([
                f'select fk_modalidade_codigo, fk_sala_codigo, fk_profissional_cpf, horario_inicio, horario_fim, dia_semana from turma_mod_sala where codigo = {turma_cod}',
                'select codigo, nome, faixa_etaria from modalidade',
                'select cpf, nome from profissional',
                'select codigo, numero, endereco from sala_unidade'
            ])

            mod_cod, sala_cod, pro_cod, horario_inicio, horario_fim, dia_semana = data[0]
        
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

            # valida dados
            if not (valid.valid_cod(modalidade) and valid.valid_cod(profissional) and valid.valid_cod(sala) and horario_inicio != '' and horario_fim != '' and dia_semana != ''):
                session['messages'] = 'Dados inválidos'
                return redirect('/')

            # updates
            db.query([
                f"update turma set fk_modalidade_codigo={modalidade} where codigo={turma_cod}",
                f"update conduz set fk_profissional_cpf='{profissional}' where fk_turma_codigo={turma_cod}",
                f"update utiliza set fk_sala_codigo={sala}, horario_inicio='{horario_inicio}', horario_fim='{horario_fim}', dia_semana='{dia_semana}' where fk_turma_codigo={turma_cod}"
            ])

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
            db.query([
                f"delete from utiliza where fk_turma_codigo={turma_cod}",
                f"delete from conduz where fk_turma_codigo={turma_cod}",
                f"delete from esta_matriculado where fk_turma_codigo={turma_cod}",
                f"delete from turma where codigo={turma_cod}"
            ])

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

            # valida dados
            if not (valid.valid_nome(nome) and faixa_etaria != ''):
                session['messages'] = 'Dados inválidos'
                return redirect('/')

            db.query(["insert into modalidade(nome, faixa_etaria) values('%s','%s')" % (nome, faixa_etaria)])

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

            modalidade = db.query([f"select codigo, nome, faixa_etaria from modalidade where nome='{mod_nome}'"])[0][0]

        except:
            session['messages'] = 'Erro ao carregar dados'
            return redirect('/')

        return render_template('modalidade.html', modalidade=modalidade)

    elif request.method == 'POST':

        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        faixa_etaria = request.form.get('faixa_etaria')

        # valida dados
        if not (valid.valid_cod(codigo) and valid.valid_nome(nome) and faixa_etaria != ''):
            session['messages'] = 'Dados inválidos'
            return redirect('/')


        db.query([f"UPDATE modalidade SET nome='{nome}', faixa_etaria='{faixa_etaria}' where codigo={codigo} "])

        return redirect('/')

@app.route('/del_modalidade', methods=['POST'])
def del_modalidade():
    if request.method == 'POST':

        mod_cod = request.form.get('codigo')

        # delete
        try:
            db.query([
                f"delete from esta_matriculado where fk_turma_codigo in (select codigo from turma where fk_modalidade_codigo = {mod_cod})",
                f"delete from utiliza where fk_turma_codigo in (select codigo from turma where fk_modalidade_codigo = {mod_cod})",
                f"delete from conduz where fk_turma_codigo in (select codigo from turma where fk_modalidade_codigo={mod_cod})",
                f"delete from turma where fk_modalidade_codigo = {mod_cod}",
                f"delete from compreende where fk_modalidade_codigo = {mod_cod}",
                f"delete from modalidade where codigo = {mod_cod}"
            ])

        except:
            session['messages'] = 'Erro ao remover modalidade'
            return redirect('/')
    
        session['messages'] = 'Modalidade removida com sucesso'
        return redirect('/')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')
