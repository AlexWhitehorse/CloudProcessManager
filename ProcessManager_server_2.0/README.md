Данный файл описывает порядок развёртывания ProcessManager

1. Разместить папку ProcessManager_server в домашней директории (/home/)
2. Разместить папку ProcessManager_user в папке сервера (/var/www/html/)

3. Настройка конфигов: 
    - в ProcessManager_user/config.php
        - Изменить значение PATH_TO_PM на путь к ProcessManager_server
        Пример: const PATH_TO_PM = '/home/nameUser/ProcessManager_server/';
    
Установить sudo apt-get install php-mbstring

4. Процессы, которые нужно контролировать записывать в файл /ProcessManager_user/processes.ini

5. Добавление в автозагрузку
    `nano /lib/systemd/system/proces-manager.service`
```
[Unit]
Description=Process Manager service
After=multi-user.target
After=network.target
[Service]
Type=simple
#Environment=/home/livetv/ProcessManager_server_2.0
WorkingDirectory=/home/livetv/ProcessManager_server_2.0
ExecStart=/home/livetv/ProcessManager_server_2.0/run.sh
[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload

sudo systemctl enable proces-manager.service

sudo systemctl start proces-manager.service

sudo systemctl status proces-manager.service

    
` nano /lib/systemd/system/proces-manager-controller.service`
    
 ```
[Unit]
Description=Controller Process Manager service
After=multi-user.target
After=network.target
[Service]
Type=simple
#Environment=/home/livetv/ProcessManager_server_2.0/
WorkingDirectory=/home/transcod/ProcessManager_server_2.0/ProcessController\ GO/weberr/
ExecStart=/home/transcod/ProcessManager_server_2.0/ProcessController\ GO/weberr/dev_run.sh
[Install]
WantedBy=multi-user.target
```
```
sudo systemctl daemon-reload &
sudo systemctl enable proces-manager-controller.service &
sudo systemctl start proces-manager-controller.service &
sudo systemctl status proces-manager-controller.service 
```
