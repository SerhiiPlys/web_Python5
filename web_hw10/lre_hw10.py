import requests
import redis
from redis_lru import RedisLRU

link = "https://github.com/matyushkin/lessons/blob/master/caching/lru-cache.ipynb"

client = redis.StrictRedis(host="localhost", port=6379, password=None)
# размер кеша 1МB, время хранения 900сек, не очищать при выходе
cache = RedisLRU(client, max_size=1048576, default_ttl=900,
                 key_prefix='RedisLRU', clear_on_exit=False,
                 exclude_values=None, expire_on=None))


@cache
def get_data(url):
    print("Запрос по URL")
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # тестовый вызов процедуры с закешированием
    data_test = get_data(link)
    # loop получения данных с кешированием
    while True:
        inp = input("Введите Урлу либо N для выхода")
        if inp == "N":
            break
        data_loop = get_data(inp)
    
