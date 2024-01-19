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
