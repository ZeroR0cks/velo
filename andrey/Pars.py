import requests
from bs4 import BeautifulSoup
import csv
import re
from model import Product


def parser(url: str, total_items: int = 3428):
    create_csv()
    page = 1
    count_items = 0

    while count_items < total_items:
        list_product = []
        # Формируем URL с учетом .html для каждой страницы
        res = requests.get(f"{url}{page}.html")

        soup = BeautifulSoup(res.text, "lxml")
        products = soup.find_all("div", class_="product-card")

        if not products:  # Если на странице нет продуктов, завершить работу
            break

        for product in products:
            # Проверяем, что это велосипед
            velo = product.find("div", class_="product-card__category")
            if velo and "горный велосипед" in velo.get_text(strip=True).lower():
                name = product.find("div", class_="product-card__model")
                if name:
                    name_text = name.get_text(strip=True)
                    # Извлекаем год из названия с помощью регулярного выражения
                    year = extract_year_from_name(name_text)

                    # Цена товара
                    price_tag = product.find("meta", itemprop="lowPrice")
                    if price_tag:
                        price = price_tag.get("content")
                        if price == "0" or not price:
                            price = "Нет в наличии"
                    else:
                        price = "Нет в наличии"

                    # Ссылка на товар
                    link_tag = product.find("a", class_="product-card__title")
                    link = link_tag.get("href") if link_tag else "Ссылка не найдена"
                    # Добавление информации о товаре в список
                    ful_link = f"https://www.velostrana.ru{link}"  # Убедитесь, что ссылка абсолютная
                    image_tag = product.find("img", itemprop="image")
                    image_url = image_tag.get("src")
                    if image_url == "/assets/images/server_s_foto.svg":
                        image_url = "https://fitowatt.ru/assets/static/noimage.jpg"
                    # Добавляем год в Product
                    list_product.append(Product(name=name_text, link=ful_link, price=price, image=image_url, year=year))
                    count_items += 1
                    print(
                        f"Обработан товар {count_items}: {name_text}, Цена: {price}, Ссылка: {ful_link}, Изображение {image_url}, Год: {year}")
                    if count_items >= total_items:
                        break  # Если достигнуто необходимое количество товаров, прерываем цикл

        # Запись данных в CSV после обработки страницы
        write_csv(list_product)
        page += 1  # Переходим к следующей странице


def create_csv():
    with open(f".venv/glavsanab.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([  # Заголовки столбцов
            "name",
            "link",
            "price",
            "image",
            "year"
        ])


def write_csv(products: list[Product]):
    with open(f".venv/glavsanab.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([product.name, product.link, product.price, product.image, product.year])


def extract_year_from_name(name: str) -> str:
    """
    Функция для извлечения года из названия товара в формате "(год)".
    Если год не найден, возвращается "Не указан".
    """
    match = re.search(r"\((\d{4})\)$", name)  # Ищем год в конце строки в круглых скобках
    if match:
        return match.group(1)
    return "Не указан"


if __name__ == "__main__":
    parser(url="https://www.velostrana.ru/gornye-velosipedy/")
