# vkBot - бот рассылки постов ВКонтакте

## Инструкция по использованию

1. Устанавливаем python 3.8 или выше
2. Устанавливаем нужные библиотеки ```pip install -r requirements.txt```
3. Далее делаем **первичную** настройку:
   - #### Получаем токен:
     1. Переходим по [ссылке](https://oauth.vk.com/authorize?client_id=7951582&display=page&redirect_uri=http://vk.com/ernestlistvinenko&scope=groups,wall,photos,offline&response_type=token&v=5.65)
     2. Выполняем вход в аккаунт
     3. Соглашаемся с правами доступа
     4. И копируем из аддресной строки access_token
        >http://REDIRECT_URI#access_token= ***533bacf01e11f55b536a565b57531ad114461ae8736d6506a3***&expires_in=86400&user_id=8492&state=123456
        
        Данную строку мы должны скопировать и вставить в переменную TOKEN в main.py

        ```python
        # Вставьте ваш токен сюда
        TOKEN = "YOUR_TOKEN"
        ```
        Строка должна принять вид:
        ```python
        # Вставьте ваш токен сюда
        TOKEN = "533bacf01e11f55b536a565b57531ad114461ae8736d6506a3"
        ```
    - #### Логин и пароль
        - В main.py находим строки:
            ```python
            LOGIN = 'YOUR_VK_LOGIN'
            PWD = 'YOUR_VK_PASSWORD'
            ``` 
            Как и следует из названия, вставляем логин и пароль от VK
    - #### Группы, текст поста и изображения (assets)
        > В данной секции мы будем говорить о тех вещах которые необходимо закидывать в папку **assets/**
      - Группы находится в файле group.txt
          >Важно добавлять группы исключительно в формате ссылки, то есть **https://vk.com/ernestlitvinenko**.
           
        >Обязательно группы разделять переносом строки и **не оставлять** пустых строк между ссылками, иначе скрипт не поймет вход данных.
      - Текст поста необходимо добавлять в файл piar.txt
      - ##### Изображения
        - Важно изображения расположить в папке assets и в переменной: 
            ```python
                PHOTO_FILEPATH = 'image.jpg' 
            ```
            Указать имя вашего изображения

#####  Надеюсь вам помогла данная документация! Удачи в ваших опытах!
> CREATED AND COPYRIGHTED BY ERNEST LITVINENKO
> 
> VK: https://vk.com/ernestlitvinenko
