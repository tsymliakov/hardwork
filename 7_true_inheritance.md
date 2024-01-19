Рассмотрим библиотеку logging для python.

Существует базовый класс Handler:

``` python
class Handler(Filterer):

    # всякие методы до

    def emit(self, record):
        """
        Do whatever it takes to actually log the specified logging record.

        This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.
        """
        raise NotImplementedError('emit must be implemented '
                                  'by Handler subclasses')

    # всякие методы после

```


Метод emit этого класса не определен, точнее определен, но призван выбрасывать исключение. Все его наследники переопределяют этот метод. Происходит "неистинное" наследование.


``` python
class OSSysLogHandler(logging.Handler):
    # Тут переопределяется конструктор

    def emit(self, record):
        priority = SYSLOG_MAP.get(record.levelname, 7)
        message = self.format(record)
        syslog.syslog(priority, message)
```

# Применение Visitor

С помощью паттерна Visitor возможно уйти от неистинного наследования к истинному в контексте этого метода. Расширив возможности постетителя, можно совершить аналогичную процедуру и с другими методами.

Для этого следует определить класс Visitor с методами отправки, соответствующими классам- наследникам класса Handler.

``` python
class Visitor:
    def emit_file_handler():
        ...
    def emit_syslog_handler():
        ...
```

В базовом классе Handler следует определить абстрактный метод, вызывающий посетителя.

``` python
class Handler(Filterer):
    def get_visit(self, visitor):
        raise NotImplementedError()
```

А в наследниках Handler'а необходимо использовать конкретные методы посетителя.

``` python
class FileHandler(Handler):
    def get_visit(self, visitor):
        visitor.emit_file_handler()

class SyslogHandler(Handler):
    def get_visit(self, visitor):
        visitor.emit_syslog_handler()
```

Вообще можно было бы применить перегрузку по типу входного аргумента:

```
class Visitor:
    def emit(FileHandler h): ...
    def emit(SyslogHandler h): ...
```

Но python такое делать не позволяет.

# Если слона негде спрятать

Спустя все эти действия, методы класса Handler все равно переопределяются в наследниках, а это не соответствует заданию. Чтобы удовлетворить условию задания, сделаем следующие действия:

1) Во всех наследниках класса Handler будет один и тот же метод `visitor.visit()`.
2) Внутри класса Visitor можно было бы воспользоваться перегрузкой по параметру, но в python этого нет, поэтому воспользуемся цепочкой if'ов:

``` python
class Visitor:
    def emit_file_handler(record): ...
    def emit_syslog_handler(record): ...

    def visit(self, handler, record):
        if type(handler) is OSSysLogHandler:
            emit_syslog_handler(record)
            ...
        else if type(handler) is FileHandler:
            emit_file_handler(record)
            ...
```

А если заменить цепочку if-else'ов на сопоставление типа с подобие паттерн-мэтчинга, то получится даже чуть более красиво:

``` python
class Visitor:
    # методы

    emit_method = {
        OSSysLogHandler: emit_syslog_handler,
        FileHandler: emit_file_handler
    }

    def visit(self, handler, record):
        emit_method.get(type(handler))(record)

```
