Данный файл описывает порядок развёртывания ProcessManager

1. Разместить папку ProcessManager_server в домашней директории (/home/)
2. Разместить папку ProcessManager_user в папке сервера (/var/www/html/)

3. Автоустановка зависимостей:
    - chmod +x ./myscript
    - ./installDepends.sh

4. Настройка конфигов: 
    - в ProcessManager_user/config.php
        - Изменить значение PATH_TO_PM на путь к ProcessManager_server
        Пример: const PATH_TO_PM = '/home/nameUser/ProcessManager_server/';

5. Процессы, которые нужно контролировать записывать в файл /ProcessManager_user/processes.ini

6. Ошибки необходимо вписывать в файл /ProcessManager_server/errors.json

7. Первый запуск программы рекомендуеться производить с правами sudo
    - sudo python3 main.py




-- version 1.0 /ProcessManager was originally written by Alex Bielokone <sasha.belokone@gmail.com>