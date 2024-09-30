# Importando a biblioteca pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Função para conectar ao MongoDB local
def connect_mongo():
    try:
        # Conectar ao servidor MongoDB local na porta padrão (27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Nome do banco de dados
        db = client['nome_do_banco_de_dados']  # Substitua pelo nome do seu banco de dados
        
        print("Conexão com o MongoDB foi bem-sucedida!")
        return db
    
    except PyMongoError as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None


