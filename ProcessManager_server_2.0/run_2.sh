#!/bin/sh
cd ProcessController\ GO/weberr/;
echo PATH;
sudo ./dev_run.cmd &
sd ..;
cd ..;
sleep 3;
python3 main.py
