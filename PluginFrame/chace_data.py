import json
import os
import time

cache_data = {}
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def init_cache():
    global cache_data
    if os.path.isfile(os.path.join(path, "data/cache_data.json")):
        with open(os.path.join(path, "data/cache_data.json"), 'r', encoding='utf-8') as f:
            time.sleep(1)
            text = f.read()
            cache_data = json.loads(text)


def set_cache(key, value):
    cache_data[key] = value
    with open(os.path.join(path, "data/cache_data.json"), 'w', encoding='utf-8') as f:
        json.dump(cache_data, f)
    return True


def get_cache(key):
    global cache_data
    return cache_data.get(key)


def del_cache(key):
    global cache_data
    if get_cache(key):
        cache_data.pop(key)

    with open(os.path.join(path, "data/cache_data.json"), 'w', encoding='utf-8') as f:
        json.dump(cache_data, f)
    return True
