#Cloud Process Manager for Live-tv Service
- Python 3.7+ | GO 
- PHP | JS + Jquery | Bootstrap
- Linux, Ubuntu tested
- Free port 65204

# Описание
Менеджер процессов для ffmpeg. 

- Веб интерфейс
	- Запуск/остановка процессов
	- Мониторинг статуса процесса
	- Просмотр логов ffmpeg
	- Разделение процессов на пользователей
	- Суперпользователь
	
- Дополнительные возмодности
	- Автостарт при непредвиденной перезагрузке
	- Проверка процессов на остановку => рестарт
	- Контроль ошибок в логах ffmpeg. При достижении лимита за N период времени => рестарт

# Порядок развёртывания ProcessManager

1. Разместить папку ProcessManager_server в домашней директории (/home/)
2. Разместить папку ProcessManager_user в папке сервера (/var/www/html/)

3. Настройка конфигов: 
В ProcessManager_user/config.php
Изменить значение PATH_TO_PM на путь к ProcessManager_server
Пример: 
```
const PATH_TO_PM = '/home/nameUser/ProcessManager_server/';
```
    
Установить
```
sudo apt-get install php-mbstring
```

4. Процессы которые нужно контролировать записывать в файл ***/ProcessManager_user/processes.ini***

## Добавление в автозагрузку
```
    sudo nano /lib/systemd/system/proces-manager.service
```

```
[Unit]
Description=Process Manager service
After=multi-user.target
After=network.target

[Service]
Type=simple

#Путь к директории ProcessManager_server_2.0
WorkingDirectory=/home/

#Путь к файлу сценария run.sh
ExecStart=/home/.../run.sh

[Install]
WantedBy=multi-user.target
```
```
sudo systemctl daemon-reload
```
```
sudo systemctl enable proces-manager.service
```
```
sudo systemctl start proces-manager.service
```

