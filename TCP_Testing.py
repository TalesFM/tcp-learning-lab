import socket
import threading
import time


# ============================================================
# CONFIGURAÇÕES DO LABORATÓRIO
# ============================================================

# IP DA INTERFACE DE REDE LOCAL DO COMPUTADOR
SERVER_IP = "192.168.0.57"

# PORTA TCP QUE SERÁ UTILIZADA PELO SERVIDOR
PORT = 5000


# ============================================================
# FUNÇÃO DO SERVIDOR TCP
# ============================================================

def server():

    # CRIA UM SOCKET TCP
    # AF_INET = IPV4
    # SOCK_STREAM = TCP
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # ASSOCIA O SOCKET AO IP E À PORTA DEFINIDOS
    server_socket.bind((SERVER_IP, PORT))

    # COLOCA O SOCKET EM MODO DE ESCUTA
    # O SERVIDOR AGUARDA UMA CONEXÃO DE UM CLIENTE
    server_socket.listen(1)

    print(f"[SERVER] LISTENING ON {SERVER_IP}:{PORT}")

    # ACEITA UMA CONEXÃO TCP
    # O PROGRAMA FICA BLOQUEADO AQUI ATÉ O CLIENTE SE CONECTAR
    connection, address = server_socket.accept()

    print(f"[SERVER] CONNECTION FROM {address}")

    # RECEBE DADOS ENVIADOS PELO CLIENTE
    # 1024 = QUANTIDADE MÁXIMA DE BYTES RECEBIDOS NESTA LEITURA
    data = connection.recv(1024)

    # CONVERTE OS BYTES RECEBIDOS PARA TEXTO
    print(f"[SERVER] RECEIVED: {data.decode()}")

    # CRIA A MENSAGEM QUE SERÁ ENVIADA DE VOLTA AO CLIENTE
    response = b"HELLO FROM SERVER!"

    # ENVIA OS DADOS PELO SOCKET TCP
    connection.sendall(response)

    print("[SERVER] RESPONSE SENT")

    # FECHA A CONEXÃO COM O CLIENTE
    connection.close()

    # FECHA O SOCKET DO SERVIDOR
    server_socket.close()

    print("[SERVER] SERVER CLOSED")


# ============================================================
# FUNÇÃO DO CLIENTE TCP
# ============================================================

def client():

    # ESPERA UM SEGUNDO PARA DAR TEMPO DO SERVIDOR
    # TERMINAR DE CONFIGURAR O SOCKET E ENTRAR EM LISTEN
    time.sleep(1)

    # CRIA UM SOCKET TCP
    # AF_INET = IPV4
    # SOCK_STREAM = TCP
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    print(f"[CLIENT] CONNECTING TO {SERVER_IP}:{PORT}")

    # INICIA A CONEXÃO TCP COM O SERVIDOR
    # AQUI ACONTECE O PROCESSO DE ESTABELECIMENTO DA CONEXÃO
    # SYN -> SYN/ACK -> ACK
    client_socket.connect((SERVER_IP, PORT))

    print("[CLIENT] CONNECTION ESTABLISHED")

    # MENSAGEM QUE SERÁ ENVIADA AO SERVIDOR
    # O SOCKET TCP TRABALHA COM BYTES
    message = b"HELLO FROM CLIENT!"

    # ENVIA A MENSAGEM PELO SOCKET TCP
    client_socket.sendall(message)

    print("[CLIENT] MESSAGE SENT")

    # AGUARDA A RESPOSTA DO SERVIDOR
    response = client_socket.recv(1024)

    # CONVERTE OS BYTES RECEBIDOS PARA TEXTO
    print(f"[CLIENT] RECEIVED: {response.decode()}")

    # FECHA O SOCKET DO CLIENTE
    # ISSO PARTICIPA DO PROCESSO DE ENCERRAMENTO DA CONEXÃO TCP
    client_socket.close()

    print("[CLIENT] CLIENT CLOSED")


# ============================================================
# CRIAÇÃO DAS THREADS
# ============================================================

# CRIA UMA THREAD PARA EXECUTAR O SERVIDOR
server_thread = threading.Thread(target=server)

# CRIA UMA THREAD PARA EXECUTAR O CLIENTE
client_thread = threading.Thread(target=client)


# ============================================================
# INICIALIZAÇÃO DO SERVIDOR E DO CLIENTE
# ============================================================

# INICIA A THREAD DO SERVIDOR
server_thread.start()

# INICIA A THREAD DO CLIENTE
client_thread.start()


# ============================================================
# AGUARDA AS DUAS THREADS TERMINAREM
# ============================================================

# O PROGRAMA ESPERA O SERVIDOR TERMINAR
server_thread.join()

# O PROGRAMA ESPERA O CLIENTE TERMINAR
client_thread.join()


# ============================================================
# FINALIZAÇÃO DO LABORATÓRIO
# ============================================================

print("[MAIN] TCP COMMUNICATION FINISHED")
