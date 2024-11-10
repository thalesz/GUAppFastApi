from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha:str, hash_senha:str)-> bool:
    """
        verifica para verificar se a senha esta correta comparando a senha em texto 
        puro e o hash que estara salvo no banco de dados durante a criação da cinta
    """
    
    return CRIPTO.verify(senha, hash_senha) 

def gerar_hash_snha(senha:str)->str:
    "funcao que gera e retorna o hash da senha"
    
    return CRIPTO.hash(senha)

