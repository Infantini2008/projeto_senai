import psycopg2


# Sua URL de conexão
DB_URL = "postgres://avnadmin:AVNS_T6QHOhUgvDRVXGUQXLA@pg-174877d1-app-consumo.d.aivencloud.com:17956/defaultdb?sslmode=require"

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
    # Sempre feche a conexão ao terminar
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("Conexão encerrada.")