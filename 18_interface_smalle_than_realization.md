# Призрачное состояние

### 1

Реализую cross join внутри кода, потому что ORM на это не способна. Вообще- то мне и cross join не требуется для решения задачи, но хорошая мысль приходит опосля.

``` python
user_point_sums = session.execute(stmt).all()
# SQLAlchemy нативно и без костылей не поддерживает cross- join.

cross_joined = []

for i in range(len(user_point_sums)):
    for j in range(len(user_point_sums)):
        ...
```

### 2

Внутри эндпоинта использую призрачное состояние в виде сессии, таким образом выходит, что половина кода у меня происходит вне сессии, другая половина внутри, а что самое важное- со стороны может быть не ясно, а какой код необходимо исполнять пока сессия жива, а какой можно исполнить после закрытия сессии.

``` python
with session_factory() as session:
    stmt = select(UserAchievement).filter(UserAchievement.awarding_datetime >= start_date, UserAchievement.awarding_datetime <= end_date)
   result = session.execute(stmt)
```

# Суживающие неточности

### 1

В общем- у меня есть с десяток примеров энпоинтов, в которых я не ожидаю, что данных в таблице может и не оказаться. Таким образом, мой интерфейс спроектирован с жестким ограничением "данные есть". Его следует переделать, расширив количество возможных состояний.

### 2

Этот эндпоинт выдает информацию о достижениях пользователя на том языке, который он когда- то там давно указывал. Проблема кода заключается в том, что может произойти проблема- в новых версиях приложения будет отсутствовать поддержка выбранного языка, например из- за политики отмены :)

В общем плохо, следует изменить интерфейс.

``` python
with session_factory() as session:
        user = session.get(User, id)

        user_lang = user.language
        print(user_lang)

        for ach in user.user_achievements:
            user_lang_achievement = getattr(ach, f"{user_lang}_achievement")
            ach.description = user_lang_achievement.description
        return user
```

### 3

Кусок ниже приведенного кода является куском эндпоинта, который вычисляет двух пользователей с наименьшим и наибольшим показателем переменной point.

Фактическая спецификация эндпоинта говорит: "есть два особых пользователя, дай мне их". Но что, если пользователей меньше двух? Эту ситуацию мой эндпоинт не обрабатывает.

``` python
    result = session.execute(stmt).all()
    max_points_sum_user_id = result[0]
    min_points_sum_user_id = result[-1]
```

# Интерфейс должен быть сложнее реализации


### 1

Такую ситуацию я встречаю в коде своих коллег, программирующих на Си под микроконтроллер, там люди в функции пихают чуть ли не сырые 7 байт, а внутри функции "знают", что им интересен третий и пятый байты.

В этом случае точно требуется усложнение интерфейса посредством типа (структуры).

## 2

Этот прием пригодился бы в функциях реализации криптографии с моей работы, там по всему коду передаются магические числа, которые на самом деле обладают особым математическим смыслом.

Улучшить эту ситуацию можно было бы создав пару классов или на худой конец, хотя бы, использовать значащее имя для переменной.

## 3

Довелось мне наблюдать код одного проекта на JS и PHP, в котором выводились миниатюры домов. Вид миниатюры (одна картинка или другая) вычислялся на основе значения pop_item, который был равен 1 или 2. Таким образом, функция ожидала в качестве параметра целочисленное значение, если оно равнялось 2- выводилась картинка большого дома, во всех остальных случаях выводилась картинка малого дома.
