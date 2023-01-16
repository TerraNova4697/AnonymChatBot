# AnonymChatBot

<h2>Краткое ТЗ</h2>

Бот для анонимного общения. К общению допускаются только те, кто пройдет тест. Идея в том, чтобы людям, схожим по интересам, дать возможность анонимно общаться. Следовательно, после успешного прохождения теста, пользователю предлагается заполнить анкету, где он указывает, какого собеседника он/она хотел/а бы. После чего бот из общего пула пользователей находит наиболее подходящих и предлагает им вступить в переписку. В процессе переписки пользователи могут либо выйти из чата, либо обменятсья номерами. Обмен происходит только если оба нажали соответствующую кнопку. 

<h2>Реализация</h2>

На момент начала работы у заказчика еще не было конечной картины продукта. Мы определились с этим вместе, в процессе разговора. 

Основной сложностью мне виделась именно логика состояний каждого пользователя. Также ожидалось, что бот будет достаточно нагруженным.
Обе эти задачи, на мой взгляд хорошо решались с помощью асинхронной библиотеки aiogram, в которой есть встроенный, удобный инструмент управления состоянием пользователя.

<h2>Что получилось</h2>

1) Бот, в котором пользователь допускается к чату только после успешного прохождения теста. 
2) Возможность подобрать собеседника по своим критериям.
3) Анонимный чат.
4) Встроенная возможность обменяться контактами.

<h2>Какие технологии использовались</h2>

Python<br>
Telegram Bot API<br>
aiogram<br>
apscheduler<br>

<h2>Скрины</h2>
