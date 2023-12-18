На работе мне приходится писать кодовые файлы с применением Rainer Script. Эти
файлы задают правила обработки логов в ходе интерпретации rsyslog'ом. Сперва
мой код выглядел очень просто, логи шлются на первый сервер, в случае ошибки,
они шлются на второй или на третий, если и со вторым возникла проблема.

```
action(type="omfwd" Target="logging01" Port="514" Protocol="tcp")
action(type="omfwd" Target="logging02" Port="514" Protocol="tcp"
       action.execOnlyWhenPreviousIsSuspended="on")
action(type="omfwd" Target="logging03" Port="514" Protocol="tcp"
       action.execOnlyWhenPreviousIsSuspended="on")
```

Время от времени мне приходится отлаживать мой код. Для этого, еще когда я думал, что один раз отладиться мне будет достаточно, я вписывал и удалял следующего вида директиву:

```
template(name="debug_template" type="string" string="%rawmsg%")
action(type="omfile" file="/tmp/debug.log" Template="debug_template")
```

Затем я перешел к тому, что эти две строки можно комментировать и откомментировать при необходимости.

Если описывать суть, политику или дизайн rsyslog'а, то это удобнее всего сделать, нарисовав дорогу, по которой едут сообщения, а также множество поворотов, на которых копии логов могут свернуть. Именно такая картинка хранится в одном из материалов на официальном сайте.

Я придумал реализовать этот дизайн в рамках кодового файла для rsyslog. Я сделал два ruleset, и два тумблера, которыми можно их отключать и включать.

Эта идея казалась мне логичной, но почему- не ясно. После вникания в материал из Сильных Идей и в текст текущего задания, кажется, я могу сказать, что подсознательно понял уже заложенный дизайн в rsyslog и не отошел от него в ходе реализации своей задумки.

```
ruleset(name="tcp-client-ruleset"){
    action(type="omfwd"
        Target="logging01"
        Port="514"
        Protocol="tcp")

    action(type="omfwd"
        Target="logging02"
        Port="514"
        Protocol="tcp"
        action.execOnlyWhenPreviousIsSuspended="on")

    action(type="omfwd"
        Target="logging03"
        Port="514"
        Protocol="tcp"
        action.execOnlyWhenPreviousIsSuspended="on")
}

ruleset(name="debug-ruleset"){
    action(type="omfile"
           file="/tmp/debug.log")
}

# Trust me, it is the most comfortable way to configure it. Also you
# can use getenv('SOME_ENV') to get system environment, but in
# this case you have to reboot your system to update system
# environments

if "no" == "yes" then {
    call debug-ruleset
}

if "yes" == "yes" then {
    call tcp-client-ruleset
}
```

Идеально было бы, конечно, вынести эту логику и вовсе в отдельный модуль, с которым бы собирался rsyslog, но для этого придется писать много кода на Си. В этом случае трудозатраты сильно превысили бы получаемый результат.
