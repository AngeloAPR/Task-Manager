import mysql.connector
import datetime

config = {
    'user': 'root',
    'password': 'Caricoa17_!',
    'host': 'localhost',
    'database': 'dados'
}

def conectar():
    try:
        conexao = mysql.connector.connect(**config)
        print("Conexão estabelecida com sucesso!")
        return conexao
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao banco de dados:", erro)

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                descricao TEXT,
                completa BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
        print("Tabela 'tarefas' criada com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao criar tabela:", erro)

def adicionar_tarefa():
    titulo = input("Digite o título da tarefa: ")
    descricao = input("Digite a descrição da tarefa: ")
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO tarefas (titulo, descricao)
            VALUES (%s, %s)
        """, (titulo, descricao))
        conexao.commit()
        print("Tarefa adicionada com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao adicionar tarefa:", erro)

def exibir_tarefas():
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()
        
        if len(tarefas) == 0:
            print("Nenhuma tarefa encontrada.")
        else:
            for tarefa in tarefas:
                id, titulo, descricao, completa = tarefa
                status = 'Completa' if completa else 'Incompleta'
                print(f"{id}. {titulo} - {status}")
    except mysql.connector.Error as erro:
        print("Erro ao exibir tarefas:", erro)

def concluir_tarefa():
    tarefa_id = input("Digite o ID da tarefa a ser concluída: ")
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("UPDATE tarefas SET completa = TRUE WHERE id = %s", (tarefa_id,))
        conexao.commit()
        print("Tarefa concluída com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao concluir tarefa:", erro)

def apagar_tarefa():
    tarefa_id = input("Digite o ID da tarefa a ser apagada: ")
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
        conexao.commit()
        print("Tarefa apagada com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao apagar tarefa:", erro)

def realizar_backup():
    conexao = conectar()
    cursor = conexao.cursor()
    
    data_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"backup_tarefas_{data_hora}.sql"
    
    try:
        with open(nome_arquivo, "w") as arquivo:
            cursor.execute("SELECT * FROM tarefas")
            tarefas = cursor.fetchall()
            
            for tarefa in tarefas:
                id, titulo, descricao, completa = tarefa
                linha = f"{id},'{titulo}','{descricao}',{completa}\n"
                arquivo.write(linha)
        
        print(f"Backup realizado com sucesso. Arquivo: {nome_arquivo}")
    except mysql.connector.Error as erro:
        print("Erro ao realizar backup:", erro)

def menu():
    criar_tabela()
    
    while True:
        print("\n=== Sistema de Gerenciamento de Tarefas ===")
        print("1. Adicionar Tarefa")
        print("2. Exibir Tarefas")
        print("3. Concluir Tarefa")
        print("4. Apagar Tarefa")
        print("5. Realizar Backup")
        print("0. Sair")

        opcao = input("Digite a opção desejada: ")
        
        if opcao == '1':
            adicionar_tarefa()
        elif opcao == '2':
            exibir_tarefas()
        elif opcao == '3':
            concluir_tarefa()
        elif opcao == '4':
            apagar_tarefa()
        elif opcao == '5':
            realizar_backup()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Digite novamente.")

if __name__ == "__main__":
    menu()
