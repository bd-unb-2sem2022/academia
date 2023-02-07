
def valid_cpf(cpf:str) -> bool:
    return len(cpf) == 11 and cpf.isdigit()

def valid_nome(nome:str) -> bool:
    return len(nome) >= 2 and len(nome) < 50 and not nome.isdigit()
    
def valid_cod(cod:str) -> bool:
    return cod.isdigit()
