# Бот Арбузер

Иногда в жизни детей происходят сложные ситуации, которые негативно влияют на их эмоциональное и психологическое
состояние. В такое время дети ищут помощи и не всегда могут обратиться напрямую к родителям или психологам. С помощью
нашего бота дети смогут анонимно связываться с психологом, который окажет необходимую помощь и подскажет ребенку по всем
интересующим вопросам.

### Развертка приложения

1) Скопировать .env.prod и переименовать его в .env
2) Вставить в .env токен телеграм бота
3) Установить библиотеки из requirements.txt
   `pip install -r requirements.txt`
4) Развернуть docker контейнер(См. help_docker.txt)
   `docker-compose up --build`
5) Запустить UserPhrase и User
6) Запустить Seeder_Admin
7) Из папки bot запустить main.py