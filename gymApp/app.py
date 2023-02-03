from flask import Flask, render_template

from db import conexao

app = Flask(__name__)

cursor = conexao.cursor()

# routes
@app.route('/')
def index():
    cursor.execute('select aluno, turma_codigo, modalidade, unidade_nome from nome_aluno_modalidade_unidade')
    res = cursor.fetchall()
    return render_template('index.html', alunos=res)



