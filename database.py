import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Busca a URL da variável de ambiente
DB_URL = os.getenv("DB_URL")

try:
    # Estabelecendo a conexão
    connection = psycopg2.connect(DB_URL)
    
    # Criando um cursor para executar comandos
    cursor = connection.cursor()
    
    # Teste: Verificando a versão do PostgreSQL
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"Conectado ao: {record}")

except Exception as error:
    print(f"Erro ao conectar: {error}")

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("Conexão encerrada.")