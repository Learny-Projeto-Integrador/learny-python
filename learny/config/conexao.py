from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Substitua pela sua string de conexão
mongo_uri = "mongodb+srv://joao:admin@cluster0.jydih.mongodb.net/learny-bd?retryWrites=true&w=majority&appName=Cluster0"

try:
    # Tentar conectar ao MongoDB
    client = MongoClient(mongo_uri)
    
    # Acessar o banco de dados
    db = client["learny-bd"]
    
    # Testar a conexão
    client.admin.command('ping')
    print("Conexão realizada com sucesso!")

except PyMongoError as e:
    print("Erro ao conectar ao MongoDB:", e)

