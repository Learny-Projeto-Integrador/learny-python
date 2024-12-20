from pymongo import MongoClient
from pymongo.errors import PyMongoError

def create_connection():
    mongo_uri = "mongodb+srv://joao:admin@cluster0.jydih.mongodb.net/learny-bd?retryWrites=true&w=majority&appName=Cluster0"

    try:
        # Tentar conectar ao MongoDB
        client = MongoClient(mongo_uri)
        
        # Acessar o banco de dados
        db = client["learny-bd"]
        
        # Testar a conexão
        client.admin.command('ping')
        
        return db
    
    except PyMongoError as e:
        print("Erro ao conectar ao MongoDB:", e)
        
def close_connection(client):
    try:
        if client:
            client.close()
        else:
            print("Nenhuma conexão ativa para fechar.")
    
    except PyMongoError as e:
        print("Erro ao fechar a conexão:", e)

