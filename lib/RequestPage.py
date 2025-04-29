import requests


"""
Verifica se uma página específica existe e retorna o conteúdo.

Args:
    url (str): URL da página a ser verificada.
    
Returns:
    str: Conteúdo da página, se encontrada; caso contrário, uma mensagem de erro.
"""

def request_page(self,url):
    try:
        response = requests.get(url)

        return response.status_code, response.text

    except requests.RequestException as e:
        return f"Erro ao acessar {url}: {e}"