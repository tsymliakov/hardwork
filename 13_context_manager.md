# Пример 1. Логирование

У меня есть в загашнике код, который парсит JSON, попутно он логирует возникающие ошибки.

``` python
class JsonConfigLoader(AbstractConfigLoader):
    def _parse_config(self, config_path):
        try:
            with open(config_path) as config:
                jsn_config = json.load(config)
                input_data_folder = jsn_config.get(INPUT_DATA_DIR)

                if input_data_folder is None:
                    LOG.error('Конфигурационный файл не содержит информации о входной директории.')
                    sys.exit()

                output_folder = jsn_config.get(OUTPUT_DIR)

                if output_folder is None:
                    LOG.error('Конфигурационный файл не содержит информации о выходной директории.')
                    sys.exit()

                return input_data_folder, output_folder

        except FileNotFoundError:
            LOG.error(f'Конфигурационный файл "{config_path}" не найден.')
            sys.exit()
        except PermissionError:
            LOG.error(f'Нет достаточных прав для чтение конфигурационного файла "{config_path}".')
            sys.exit()
```

В рамках проведения рефакторинга, я хочу переработать обработку исключений PermissionError и FileNotFoundError. Во-первых я хочу вынести их в базовый класс по работе с файлами, во- вторых намереваюсь заключить логику по перехвату исключений внутрь контекстного менеджера.

``` python
class FileConfigLoader(AbstractConfigLoader):
    def _parse_config(self, config_path):
        with open(config_path) as config:
            # ... некая логика

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        if exctype is FileNotFoundError:
            LOG.error(f'Конфигурационный файл "{config_path}" не найден.')
        else if exctype is PermissionError:
            LOG.error(f'Нет достаточных прав для чтение конфигурационного файла "{config_path}".')
        LOG.info(f'Файл {config_path} успешно обработан.')
        sys.exit()
```

Теперь, унаследовавшись JSON- лоадером от этого класса, мне необходимо лишь переопределить метод `_parse_config`.

``` python
class JsonConfigLoader(AbstractConfigLoader):
    def _parse_config(self, config_path):
        with open(config_path) as config: # в случае проблем с файлом по пути config_path, ожидаемое исключение вылетит само
            jsn_config = json.load(config)
            input_data_folder = jsn_config.get(INPUT_DATA_DIR)
            output_folder = jsn_config.get(OUTPUT_DIR)
            return input_data_folder, output_folder
```

Таким образом удалось удобным образом заключить логику в управленческий шаблон. А ведь это именно то, что мне не нравилось в моем исходном коде.

# Пример 2

Стандартная библиотека подключения к БД SQLITE по какой- то причине не имеет контекстного менеджера, в следствие этого в случае возникновения проблем на стороне клиента, соединение с базой не отваливается.

``` python
import sqlite3
from contextlib import contextmanager

@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()
```

Реализация такого контекстного менеджера инкапсулирует в себе функционал по работе с базой данных.

# Пример 3

Применяя контекстный менеджер возможно работать с потоками блокируя и освобождая ресурс автоматически.

``` python
import threading

def worker():
    print("Работник выполняет задачу...")

with threading.Lock() as lock:
    lock.acquire()
    try:
        t = threading.Thread(target=worker)
        t.start()
    finally:
        lock.release()
```
