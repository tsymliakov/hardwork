Включаю только кусок кода, поскольку нет никакой необходимости включать класс целиком

## 1

``` python
class RelpDriver(notifier.Driver):
    """
    Этот класс необходим для передачи журналируемых сообщений по протоколу RELP.
    Он находится в атрибуте 'handler' объекта класса logger, как и остальные подобные драйверы.
    Включение и отключение функциональности передачи сообщений по RELP осуществляется в соответствующем приложению
    конфигурационном файле: nova.conf / neutron.conf  так далее.
    """

    def __init__(self, conf, topics, transport):
        global RSYSLOG_SERVER_PARAMS
        conf.register_opts(
            RSYSLOG_SERVER_PARAMS,
            group='oslo_messaging_notifications')
```

## 2

Автономным может быть не только класс, но и функция.

``` python
def get_distance_between_points(p1, p2):
    """
    Функция используется для вычисления длины в метрах между двумя точками на Земле.
    А также никак не учитывает кривизну поверхности и вычисляет расстояние напрямик.
    """
    llat1 = p1[0]
    llong1 = p1[1]

    llat2 = p2[0]
    llong2 = p2[1]

    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    distance = ad * EARTH_RADIUS

    return distance
```

## 3

``` python
class Command(BaseCommand):
    """
    Команда предназначена для генерации тестовых данных. Она генерирует Компании,
    автомобили для них и водителей для автомобилей.
    """

    def add_arguments(self, parser):
        parser.add_argument('enterprises_id', type=int, nargs='+',
                            help='ID of enterprises for which data will be generated. If there is \
                                no such ID it will be created and filled with data.')

    ...
```
