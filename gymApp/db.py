import psycopg2

try:
    conexao = psycopg2.connect(user="postgres",password="qwer1234",host="localhost",port="5432",database="postgres")
except:
    raise Exception('Erro de conexão com o banco')
