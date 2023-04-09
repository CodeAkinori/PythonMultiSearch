import requests
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd

# termo de busca
search_term = input("Digite o termo de busca: ")
search_term = '"' + search_term.replace(' ', '+') + '"'

# urls dos buscadores
google_url = f"https://www.google.com/search?q={search_term}"
bing_url = f"https://www.bing.com/search?q={search_term}"
yahoo_url = f"https://br.search.yahoo.com/search?p={search_term}"
duckduckgo_url = f"https://duckduckgo.com/?q={search_term}"

# lista de urls
urls = [google_url, bing_url, yahoo_url, duckduckgo_url]

# headers para simular um acesso pelo navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# fazer a requisição HTTP e extrair os resultados de busca
links_list = []
for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # extrair os links dos resultados de busca
    links_count = 0
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href is not None and href.startswith("http"):
            links_list.append(href)
            links_count += 1
            if links_count == 5:
                break

    # abrir a página de resultados de busca no navegador
    webbrowser.open_new_tab(url)

# criar um DataFrame e salvar os dados em um arquivo CSV
df = pd.DataFrame(links_list, columns=["Links"])
file_name = f"{search_term}_search_results.csv".replace('"', '')
df.to_csv(file_name, index=False)
