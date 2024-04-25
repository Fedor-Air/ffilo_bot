import requests
from bs4 import BeautifulSoup
import re


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "connection": "keep-alive"
}

City = {
    "Москва": "moskva",
    "Санкт-Петербург": "sankt_peterburg",
    "Рязань": "ryazan",
    "Нижний Новгород": "nizhniy_novgorod",
    "Казань": "kazan",
    "Ростов-на-Дону": "rostov-na-donu",
    "Калининград": "kaliningrad",
}


def get_page(url):
    session = requests.Session()
    response = session.get(url=url, headers=headers)

    with open("weather_index.html", 'w', encoding="utf-8") as file:
        file.write(response.text)

    return get_weather(url)


def get_weather(url):
    with open("weather_index.html", 'r', encoding="utf-8") as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        temp = soup.find("div", class_="information__content__temperature").text
        weather = soup.find("span", class_=re.compile("weather-icon_size-80")).get("title")

        return 1, temp.strip(), weather.strip(), url


def main(city):
    if city in City:
        return get_page(url=f"https://pogoda.mail.ru/prognoz/{City[city]}/")
    else:
        return 0, "https://pogoda.mail.ru/prognoz/"


if __name__ == "__main__":
    print(main("Москва"))
