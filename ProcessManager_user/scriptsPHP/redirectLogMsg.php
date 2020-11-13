<?php
    ini_set('error_reporting', E_ALL);
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);

    $data = json_encode($_GET['message']);
    $length = strlen($data);

    // print(json_encode($data));

    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // Создаем TCP Socket
    socket_bind($socket, 'localhost');
    $ret = socket_connect($socket, "localhost", 33334); // Устанавливаем соединение
    
    if(!$ret): print("error connecting"); die(); endif;

    $ret = socket_send($socket, $data, $length, MSG_DONTROUTE); // Отправляем $length байт из $bindata

    $read = socket_read($socket, 800, PHP_NORMAL_READ);
    // $res = MakeNormStr($read);

    socket_close($socket);

    print_r($read);
    
?>