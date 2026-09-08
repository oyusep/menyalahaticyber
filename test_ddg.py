import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8',
}

print("=== Test DuckDuckGo HTML ===")
resp = requests.get(
    'https://html.duckduckgo.com/html/?q=%22Yusep+Maulana%22',
    headers=headers, timeout=15
)
print(f"DDG Status: {resp.status_code}, Size: {len(resp.text)}")
soup = BeautifulSoup(resp.text, 'lxml')
results = soup.find_all('a', class_='result__a')
print(f"Results found: {len(results)}")
for r in results[:5]:
    href = r.get('href', '')
    if 'uddg=' in href:
        url = unquote(href.split('uddg=')[1].split('&')[0])
    else:
        url = href
    print(f"  Title: {r.get_text()[:60]}")
    print(f"  URL: {url[:80]}")

print()
print("=== Test Bing HTML ===")
resp2 = requests.get(
    'https://www.bing.com/search?q=%22Yusep+Maulana%22&count=10',
    headers=headers, timeout=15
)
print(f"Bing Status: {resp2.status_code}, Size: {len(resp2.text)}")
soup2 = BeautifulSoup(resp2.text, 'lxml')
bing_results = soup2.find_all('li', class_='b_algo')
print(f"Bing Results: {len(bing_results)}")
for r in bing_results[:5]:
    h2 = r.find('h2')
    a = r.find('a', href=True)
    if h2 and a:
        print(f"  Title: {h2.get_text()[:60]}")
        print(f"  URL: {a['href'][:80]}")
