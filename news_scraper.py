import requests
from bs4 import BeautifulSoup
import re


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "connection": "keep-alive"
}

Theme = {
    "Политика": "ria.ru/politics/",
    "В мире": "ria.ru/world/",
    "Экономика": "ria.ru/economy/",
    "Общество": "ria.ru/society/",
    "Происшествия": "ria.ru/incidents/",
    "Армия": "ria.ru/defense_safety/",
    "Наука": "ria.ru/science/",
    "Культура": "ria.ru/culture/",
    "Религия": "ria.ru/religion/",
    "Туризм": "ria.ru/tourism/",
}


def get_page(url):
    session = requests.Session()
    response = session.get(url=url, headers=headers)

    with open("news_index.html", 'w', encoding="utf-8") as file:
        file.write(response.text)


def get_articles(flag):
    with open("news_index.html", 'r', encoding="utf-8") as f:
        content = f.read()
        soup = BeautifulSoup(content, "html.parser")

        if flag == 1:
            titles = soup.find_all("span", class_=re.compile("cell-list-f__item-title|cell-list__item-title"), limit=5)
            links = soup.find_all('a', class_=re.compile("cell-list-f__item-link color-font-hover-only|cell-list__item-link color-font-hover-only"), limit=5)
        else:
            titles = soup.find_all('a', class_=re.compile("list-item__title"), limit=5)
            links = soup.find_all('a', class_=re.compile("list-item__title"), limit=5)

        articles = {}

        for i in range(len(titles)):
            articles[titles[i].text] = links[i].get('href')

        return articles


def main(theme):
    get_page(url=f"https://{Theme[theme]}")
    flag = 0
    if theme in ["Наука", "Религия", "Туризм", "Культура"]:
        flag = 1
    return get_articles(flag)


if __name__ == "__main__":
    for a in Theme.keys():
        main(a)
