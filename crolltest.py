from bs4 import BeautifulSoup
import requests

url = 'https://map.naver.com/'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup) 
else : 
    print(response.status_code)

    