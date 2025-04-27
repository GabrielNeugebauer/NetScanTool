import socket
from datetime import datetime

# Função para verificar uma porta
def scan_port(host, port):
    try:
        # Tentando se conectar ao host na porta especificada
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # Timeout de 1 segundo
        result = sock.connect_ex((host, port))  # Conectar no host e na porta
        sock.close()
        return result == 0  # Retorna True se a porta estiver aberta
    except socket.error as err:
        print(f"Erro ao conectar no {host}:{port} - {err}")
        return False

# Função para realizar o port scan em um intervalo de portas
def port_scan(host, start_port, end_port):
    print(f"Escaneando {host} de {start_port} até {end_port}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        print(f"Verificando porta {port}...")
        if scan_port(host, port):
            open_ports.append(port)
    return open_ports

# Exemplo de uso
if __name__ == "__main__":
    host = "192.168.8.1"  # Substitua pelo IP do alvo
    start_port = 20  # Primeira porta a ser verificada
    end_port = 1024  # Última porta a ser verificada

    start_time = datetime.now()
    open_ports = port_scan(host, start_port, end_port)
    end_time = datetime.now()

    print(f"\nEscaneamento concluído em {end_time - start_time}")
    if open_ports:
        print(f"Portas abertas: {open_ports}")
    else:
        print("Nenhuma porta aberta encontrada.")
