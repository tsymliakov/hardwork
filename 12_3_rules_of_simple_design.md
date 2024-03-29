# Избегание точек генерации исключений методом построения грамотного интерфейса класса

1.

В моей программе по рисованию геометрических фигур, которую я реализовывал в качестве тестового задания, я столкнулся с проблемой: не абсолютно непрозрачную фигуру можно нарисовать несколько раз. Фактически в моей программе такого не произошло бы, потому что я заранее верно прописал интерфейс и не дал пользователю возможности выстрелить себе в ногу. А логику рисования фигуры я завязал на предусловии того, что фигура еще не была нарисована. Таким образом, интерфейс класса не позволил пользователю несколько раз нарисовать одну и ту же фигуру.

2.

Программа на django, которую я сейчас реализую в рамках другого тестового задания, обращается к google диску за документом. И вот google может отказать в соединении если его заспамить коннектами,  вызвав тем самым исключение у меня в программ. Метод connect в моей программе внутри себя блокирует исполнение в случае, если за последнее время было сделано слишком много попыток соединений.

# Избегание конструкторов по- умолчанию

В любой своей программе я использую либо параметры по-умолчанию для конструкторов, чтобы инициализировать объект начальными значениями, достаточными для работы. А также выбрасываю исключения в случае, если в инициализатор попадают некорректные параметры, сигнализируя о том, что сущностью пользуются неправильно.

# Использование типов данных из системы типов проекта

1.

В программе по рисованию фигур я оперирую сущностями фигур, то есть классами. При этом я мог бы оперировать литералами `(x, y)`, рисуя ту или иную фигуру.

2.

В книге "Python. К вершинам мастерства" автор, Лусиану Ромальо говорит о том, что кортежи можно использовать не только как неизменяемые списки, но и как хранилища для данных о сущностях.

``` python
City, year, pop = ('Tokyo', '2003', '32_450_000') # информация о популяции в городе в определенный год
```

Лусиану Ромальо, видимо, высосал это из пальца, иначе я не слишком понимаю, зачем избавляться от того, что представляет ООП язык и возвращаться практически к структурам языка СИ.
