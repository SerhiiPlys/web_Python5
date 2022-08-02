import sys
import aiohttp
import asyncio
import aiohttp_jinja2
import jinja2
from src.routes import setup_routes
import configparser
from src.config import BASE_DIR
from bs4 import BeautifulSoup

#-----это пример как не зависеть от количества URL в файле ini
# делаем список корутин автоматом, но сделать так не війдет - поскольку
# html каждого сайта различный  - потому парсиннг отличается и нужно писать свою собственную корутину 
###--------database or ini------------------------
##config = configparser.ConfigParser()
##config.read('config.ini')
##
##list_url = []
##for item in config['DB']:
##    list_url.append(config.get("DB", item))
##
##print(list_url)
##
##async def get_data_web(session, url):  
##    async with session.get(url, ssl=False) as response:
##        print("Status:", response.status)
##        print("Content-type: ", response.headers['content-type'])
##
##        html = await response.text()
##        print("Body:", html[:15], "...")
##
##
##async def main():
##    async with aiohttp.ClientSession() as session:
##        corutines = [get_data_web(session, url) for url in list_url]
##        await asyncio.gather(*corutines)

#--------database or ini------------------------
conf = configparser.ConfigParser()
conf.read(BASE_DIR/'src'/'config'/'config.ini')
url1=conf.get('DB', 'URL1')
url2=conf.get('DB', 'URL2')
url3=conf.get('DB', 'URL3')

global valute
valute = {}

async def get_data_web1(session, url):
    async with session.get(url, ssl=False) as response:
        print("Status: Privatbank", response.status)
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find_all('div', class_="currency-pairs")
        name = data[0].find('div', class_="names").text.strip()[:3]
        sold = data[0].find('div', class_="purchase").text.replace('\n', '')
        sale = data[0].find('div', class_="sale").text.replace('\n', '')
        valute['bank1_eur'] = 'Privatbank '+name+' '+sold+' '+sale
        name = data[1].find('div', class_="names").text.strip()[:3]
        sold = data[1].find('div', class_="purchase").text.replace('\n', '')
        sale = data[1].find('div', class_="sale").text.replace('\n', '')
        valute['bank1_usd'] = 'Privatbank '+name+' '+sold+' '+sale
            
async def get_data_web2(session, url):
    async with session.get(url, ssl=False) as response:
        print("Status: Kredobank", response.status)
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        datas = soup.find('tbody')
        data = datas.find_all('td')
        name = data[0].text.replace('\n', '')[3:]
        sold = data[3].text.replace('\n', '')
        sale = data[2].text.replace('\n', '')
        valute['bank2_usd'] = 'Kredobank '+name+' '+sold+' '+sale
        name = data[6].text.replace('\n', '')[3:]
        sold = data[9].text.replace('\n', '')
        sale = data[8].text.replace('\n', '')
        valute['bank2_eur'] = 'Kredobank '+name+' '+sold+' '+sale

async def get_data_web3(session, url):
    async with session.get(url, ssl=False) as response:
        print("Status: UKRSibbank", response.status)
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        datas = soup.find('tbody')
        data = datas.find_all('td')
        name = data[0].text.replace('\n', '')[:3]
        sold = data[1].text.replace('\n', '')[7:12]
        sale = data[2].text.replace('\n', '')[7:12]
        valute['bank3_usd'] = 'UKRSibbank '+name+' '+sold+' '+sale
        name = data[4].text.replace('\n', '')[:3]
        sold = data[5].text.replace('\n', '')[7:12]
        sale = data[6].text.replace('\n', '')[7:12]
        valute['bank3_eur'] = 'UKRSibbank '+name+' '+sold+' '+sale
        
#----клиентская часть - получаем данные асинхронно 
async def client_part():
    async with aiohttp.ClientSession() as session:
        corutines = [get_data_web1(session, url1),
                     get_data_web2(session, url2),
                     get_data_web3(session, url3)]
        await asyncio.gather(*corutines)

if __name__ == "__main__":
    # для корректной работы async/await в системе WINDOWS
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(client_part())
##    print(valute['bank1_usd'])
##    print(valute['bank1_eur'])
##    print(valute['bank2_usd'])
##    print(valute['bank2_eur'])
##    print(valute['bank3_usd'])
##    print(valute['bank3_eur'])
    #-----здесь получены все ответы на запросы - начинаем сервер
# создание приложения
app = aiohttp.web.Application()
# переменная окружения - базовый путь как элемент словаря в приложении
app["config"] = BASE_DIR
app['valute'] = valute # глобальная видимость этой переменной
# обязательная строка взятая из документации по джинджа2
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR /'src'/'templates')))
# описание маршрутов и хендлеров к ним
setup_routes(app)
# запуск приложения
aiohttp.web.run_app(app)
