from requests import Session
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter

# фейковый заголовок, чтобы не раскрываться что мы - бот
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
# используем сессию, чтобы автоматически работать с куками
work = Session()

# перебираем пагинацию на сайте постранично
# делаем функцию-генератор, чтобы не забивать память огромными бесполезными списками -
# оптимизируем программу уже на этом этапе
def get_url():
    for index_page in range(1,5):
        # имитируем человека  - запросы к серверу раз в 3 сек
        sleep(3)
        url = f"https://belok.ua/ua/kreatin/?page={index_page}"
        response = work.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="product")
        for item in data:
            product_url = item.find("a").get("href")
            yield product_url


def main():
     ##-----подготовка файла отчета----------
    book = xlsxwriter.Workbook("report.xlsx")
    page = book.add_worksheet("креатин")

    page.set_column("A:A", 80) #url
    page.set_column("B:B", 50) #manufacterur
    page.set_column("C:C", 40) #title
    page.set_column("D:D", 20) #price
    
    row = 0  # индекс строки
    
    for url in get_url():
        response = work.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        # на сайте разная разметка для разных товаров, так что
        # data либо data_old могут быть None - пробуем парсить 2 варианта разметки
        data = soup.find("div", class_="col-xs-12 product")
        data_old = soup.find("div", class_="product-old col-xs-12 product") 
##        print(data)
##        print(data_old)
        print(url)
        if data != None: # вариант новой верстки
            data = data.find("div", class_="col-md-6 product-info") 
            manufacturer = data.find("span", class_="manufacturer").text
            title = data.find("span", class_="product-title").text
            price = data.find("span", class_="price").text
            data = (url, manufacturer, title, price,)
            page.write(row, 0, data[0])
            page.write(row, 1, data[1])
            page.write(row, 2, data[2])
            page.write(row, 3, data[3])
            row += 1
            print(manufacturer, title , price)
            print("written to file")
        elif data_old != None:  # вариант старой верстки
            data = data_old.find("div", class_="col-xs-12 col-sm-6 product-info") 
            manufacturer = data.find("span", class_="manufacturer").text
            title = data.find("span", class_="product-title").text
            data = data_old.find("div", class_="text-center price col-sm-12 col-xs-12 no-padding") 
            price = data.find("span", class_="price-current").text
            data = (url, manufacturer, title, price,)
            page.write(row, 0, data[0])
            page.write(row, 1, data[1])
            page.write(row, 2, data[2])
            page.write(row, 3, data[3])
            row += 1
            print(manufacturer, title , price)
            print("written to file")
##        inp = input("Y/N :\n")
##        if inp == "Y":
##            continue
##        else:
##            break
    book.close() 

if __name__ == "__main__":
    main()
 
    
