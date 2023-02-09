import psycopg2

try:
    conexao = psycopg2.connect(user="postgres",password="qwer1234",host="localhost",port="5432",database="postgres")
    print(" * database connected")

except:
    raise Exception('Erro de conexão com o banco')

def query(consultas: list) -> list:
    res = []
    with conexao.cursor() as cursor:
        for c in consultas:
            cursor.execute(c)
            try:
                res.append(cursor.fetchall())
            except:
                pass
                #print('not fetched')
    try:
        conexao.commit()
    except:
        pass
        #print('not commited')
        
    return res

