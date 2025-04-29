import requests
from ..lib.RequestPage import RequestsHandler # Don't working now. I need to fix this import
#from RequestPage import RequestsHandler / Working if you run the script on the same directory

handler = RequestsHandler()

def check_robots_txt(url):
    """
    Verifica o arquivo robots.txt de um site e procura por palavras-chave específicas.
    
    Args:
        url (str): URL do site a ser verificado.
        
    Returns:
        list: Lista de palavras-chave encontradas no arquivo robots.txt.
    """
    # Adiciona /robots.txt à URL
    if not url.endswith('/'):
        url += '/'
    robots_url = url + 'robots.txt'
    
    try:
        response = requests.get(robots_url)
        if response.status_code == 404:
            print(f"Arquivo robots.txt não encontrado em {robots_url}. Erro 404")
            return []
        print(f"Arquivo robots.txt encontrado em {robots_url}.")
        response.raise_for_status()  # Levanta um erro se a resposta não for 200
        text_content = response.text
        
        # Palavras-chave a serem buscadas
        keywords = ['adm', 'admin', 'login', 'dashboard', 'cpanel','cpainel']
        found_keywords = [line for line in text_content.splitlines() if any(keyword in line for keyword in keywords)]
        
        for keyword in found_keywords:
            if url.endswith('/'):
                url = url[:-1]
            complete_url = url + keyword.split(':')[1].strip()  # Extrai a URL após o ':' e remove espaços em branco
            #print(f"Verificando URL: {complete_url, type(complete_url)}") # Debugging
            code, response = handler.request_page(complete_url)
            found_pages = {}
            if code != 404:
                found_pages[complete_url]= f'resposta: {response}'
            else:
                print(f"URL não encontrada: {complete_url} - Status: {code}")
        return f'Páginas encontradas: {found_pages}'
    
    except requests.RequestException as e:
        print(f"Erro ao acessar {robots_url}: {e}")
        return []


print(check_robots_txt('http://127.0.0.1:5000'))