# Importando a biblioteca pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Função para conectar ao MongoDB local
def create_local_connection():
    try:
        # Conectar ao servidor MongoDB local na porta padrão (27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Nome do banco de dados
        db = client['learny-bd']  # Substitua pelo nome do seu banco de dados
        
        print("Conexão com o MongoDB foi bem-sucedida!")
        return client, db  # Retornar também o client para poder fechar depois
        
    except PyMongoError as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None, None

# Função para fechar a conexão
def close_connection(client):
    if client:
        client.close()
        print("Conexão com o MongoDB foi fechada.")
    else:
        print("Nenhuma conexão ativa para fechar.")


