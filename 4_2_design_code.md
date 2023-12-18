Для текущего кода у меня не нашлось его реализации, не соответствующей дизайну. Дизайн библиотеки oslo_messaging, которую я взял за основу, подразумевает использование драйверов. На драйверах ложится ответственность за отправку в "куда-то" логов. Хорошо спроектированная библиотека и правильное её использование в другом продукте позволили мне довольно быстро дополнить мою систему журналирования требуемой функциональностью. И успешно встроить её в комплексный проект. От меня потребовалось всего- то реализовать класс `RelpDriver`, после чего, по- сути, достаточно лишь указать мой новый драйвер в конфиге приложения Openstack и параметры для драйвера.

``` python
class RelpDriver(notifier.Driver):

    def __init__(self, conf, topics, transport):
        global RSYSLOG_SERVER_PARAMS
        conf.register_opts(
            RSYSLOG_SERVER_PARAMS,
            group = 'oslo_messaging_notifications')

        self.host: str = conf.oslo_messaging_notifications.host
        self.relp_port: int = conf.oslo_messaging_notifications.port
        self.client = Client(self.relp_ip, self.relp_port)
        super().__init__(conf, topics, transport)

    def notify(self, ctxt: dict, message: dict, priority: str, retry: int):
        rfc5424_message = Message_RFC5424(ctxt, message, priority).message()

        if retry == -1:
            self._send_unlimited(rfc5424_message)
            return

        while retry > -1:
            try:
                retry -= 1
                self.client.send(rfc5424_message)
                return
            except Exception:
                # TODO: нужно залогировать неудачную отправку сообщения
                self.client = Client(self.relp_ip, self.relp_port)

    def _send_unlimited(self, rfc5424_message):
        try:
            self.client.send(rfc5424_message)
            return
        except Exception:
            self.client = Client(self.relp_ip, self.relp_port)
            self.send_unlimited(rfc5424_message)
```
