import requests
from urllib.parse import urlparse


# Função para fazer login
def login(url, username, password):
    login_data = {'username': username, 'password': password}
    session = requests.Session()  # Usando uma sessão para manter cookies
    response = session.post(url + '/login', data=login_data)
    
    if response.status_code == 200:
        print(f"Login bem-sucedido para {username}")
        print(f"Redirecionado para: {response.url}")  # Captura o URL do redirecionamento
        parsed_url = urlparse(response.url)
        path_parts = parsed_url.path.strip('/').split('/')  # Divide o caminho em partes
        extracted_username = path_parts[-1]  # Assume que o username está no final do caminho
        return session, response.url  # Retorna a sessão e o URL do redirecionamento
        
    else:
        print(f"Falha no login para {username}")
        return None, None

# Função para tentar acessar o perfil de outro usuário
def test_bac(session, url, target_username):
    # Certifique-se de que a URL termina com uma barra antes de adicionar o username
    if not url.endswith('/'):
        url += '/'
    
    full_url = url + target_username
    
    # Faz o GET na URL completa
    response = session.get(full_url)
    
    # Faz o parsing da URL para obter o caminho antes do username
    parsed_url = urlparse(full_url)
    try:
        base_path = parsed_url.path.rsplit(f'/{target_username}', 1)[0]  # Divide no último ponto antes do username
    except IndexError:
        base_path = parsed_url.path  # Caso o split falhe, use o caminho completo
    
    print(f"Base URL antes do username: {base_path}")
    
    # Verifica se a resposta indica vulnerabilidade
    if response.status_code == 200:
        print(f"Vulnerabilidade encontrada! O perfil de {target_username} é acessível.")
        print("Resposta do servidor:", response.text[:200])  # Exibir uma parte da resposta
    else:
        print(f"Sem vulnerabilidade: Acesso a {target_username} foi negado.")

# Função principal que organiza o processo
def check_bac(url, valid_user, valid_password, users_to_test):
    print(f"Iniciando o escaneamento de vulnerabilidade BAC para {valid_user}...")
    
    # Fazer login com o usuário válido
    session, redirected_url = login(url, valid_user, valid_password)
    
    if session:
        print(f"URL após login: {redirected_url}")  # Exibe o URL após o redirecionamento
        base_url=redirected_url.split('/')  # Remove o último elemento da URL
        base_url.pop()  # Remove o último elemento da URL
        base_url = '/'.join(base_url)
        print(f"Base URL para testes: {base_url}")
        # Testar os outros usuários para verificar se há vazamento de dados
        for target_user in users_to_test:
            print(f"Testando acesso ao perfil de {target_user}...")
            test_bac(session, base_url, target_user)

# URLs de exemplo (mude para seu site)
url = 'http://localhost:5000'  # Altere para o site que você deseja testar
valid_user = 'user1'  # Nome de usuário com login válido
valid_password = 'password1'  # Senha para login
users_to_test = ['user2', 'user3']  # Usuários cujos perfis queremos verificar

# Rodar o escaneamento
check_bac(url, valid_user, valid_password, users_to_test)
