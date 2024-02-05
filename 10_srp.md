## Пример 1

Вызов функции `math.sqrt()` требует рефакторинга. Точнее необходимо целиком эту математику выносить в отдельную функцию с говорящим названием.

``` python
self.lamda = self.lamb * math.sqrt(sum([h.out_features for h in self.model.heads[:-1]]) / self.model.heads[-1].out_features)
```


## Пример 2

``` python
format_and_send(clients, data, formatter)
```

->

``` python
formatted_data = get_formattet_data(data, formatter)
send_to_clients(formatted_data, clients)
```

## Пример 3

``` python
json.loads(requst.get(url, allow_redirects=True))["user"]
```

->

``` python
def get_user_data(url):
    r = requst.get(url, allow_redirects=True)
    return json.loads(r)["user"]
```

## Пример 4

``` python
max_count = sessionData["aggregates"][instance_name]["metas"]["ancud:max-instances"] \
            if "ancud:max-instances" in sessionData["aggregates"][instance_name]["metas"] else 9999
```

->

``` python
DEFAULT_MAX_COUNT = 10_000

def get_max_count(sessionData):
    return sessionData["aggregates"][instance_name]["metas"].get('["ancud:max-instances"]') or DEFAULT_MAX_COUNT
```

## Пример 5


``` python
msg = get_splited_messages_way1(msg1, msg2) if way1 else get_splited_messages_way2(msg1, msg2)
```

->

``` python
def get_splited_messages(msg1, msg2, use_way_1, split_way1, split_way2):
    if use_way_1:
        return split_way1(msg1, msg2)

    return split_way2(msg1, msg2)
```
