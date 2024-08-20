from bs4 import BeautifulSoup
import requests
from openpyexcel import load_workbook
headers = {"Accept": "*/*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


class Category:
    def __init__(self, link, name):
        self.link = link
        self.name = name

    def __str__(self):
        return self.link

def get_bs(url):
    req = requests.get(url, headers)
    src = req.text
    return BeautifulSoup(src, "lxml")


def get_restaurants_links(page):
    link_classes = page.find(class_="category-page__pagination-wrapper").find_all(class_="store-card")
    links = []
    for link in link_classes:
        links.append(f"https://glovoapp.com{link.get('href')}")
    return links


def save_restaurant_info(link, wb):
    global i
    page = get_bs(link)
    ws = wb['Restaurants']
    name = page.find(class_="store-info__title").text.strip()
    try:
        rating = page.find(class_="store-rating__label").text.strip()
    except AttributeError:
        rating = ""
    ws.append([i, name, rating, link])
    return None


def get_categories(link):
    page = get_bs(link)
    categories = []
    categories_classes = page.find_all(class_="collection__child__button collection__child__button--selected")
    for category_class in categories_classes:
        categories.append(Category(f"https://glovoapp.com{category_class.get('href')}", category_class.find(class_= "collection__child-label collection__child-label--selected").next.text.strip()))
    return categories


def save_restaurant_menu(link, wb):
    global j
    global i
    ws = wb['Menu']
    restaurant_categories = get_categories(link)
    if restaurant_categories[0].name == "МЕНЮ":
        restaurant_categories = get_bs(restaurant_categories[0].link).find_all(class_="list", type="LIST")
        for category in restaurant_categories:
            dishes_classes = category.find_all(class_="product-row")
            for dish in dishes_classes:
                name = dish.find(class_="product-row__name").next.next.text.strip()
                price = dish.find(class_="product-price__effective product-price__effective--new-card").text.strip()
                try:
                    description = dish.find(class_="product-row__info__description").next.text.strip()
                except AttributeError:
                    description = ""
                ws.append([j, i, name, description, price, category.find(class_="list__title").text.strip(), ""])
                j += 1
    else:
        for category in restaurant_categories:
            category_page = get_bs(category.link)
            dishes_classes = category_page.find_all(class_="product-row")
            for dish in dishes_classes:
                name = dish.find(class_="product-row__name").next.next.text.strip()
                price = dish.find(class_="product-price__effective product-price__effective--new-card").text.strip()
                try:
                    description = dish.find(class_="product-row__info__description").next.text.strip()
                except AttributeError:
                    description = ""
                ws.append([j, i, name, description, price, category.name, ""])
                j += 1
    return None


"""wb = load_workbook("Restaurants_database.xlsx")
ws = wb['Restaurants']
ws.append(["ID", "Name", "Rating", "Link"])
ws = wb['Menu']
ws.append(["ID", "ID_Rest", "Name", "Description", "Price", "Category", "Specifics"])

restaurant_links = []
for i in range(11):
    page = get_bs(f"https://glovoapp.com/ua/uk/lviv/restorani_1/?page={i+1}")
    restaurant_links.extend(get_restaurants_links(page))
    print(f"#{i+1} done")
print(len(restaurant_links))
i = 1
j = 1
for link in restaurant_links:
    try:
        save_restaurant_info(link, wb)
    except Exception as e:
        print(f"Rest: {e}")
        print(link)
        continue
    try:
        save_restaurant_menu(link, wb)
    except Exception as e:
        print(f"Menu: {e}")
        i += 1
        continue
    print(f"Rest#{i} done!")
    i += 1
    wb.save("Restaurants_database.xlsx")
wb.save("Restaurants_database.xlsx")
wb.close()"""
print(get_bs(get_categories("https://glovoapp.com/ua/uk/lviv/shaurmalviv-lvi?content=menyu-c.1217032060&section=shaurma-s.2831711184")[0].link))

