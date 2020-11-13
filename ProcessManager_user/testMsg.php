<?php
    ini_set('error_reporting', E_ALL);
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);

    

    function sendData($array)
    {
        $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // Создаем TCP Socket
        $ret = socket_connect($socket, "localhost", 65204); // Устанавливаем соединение
        
        if(!$ret): print("error connecting"); die(); endif;

        $data = json_encode($array);

        // sudo apt-get install php-mbstring
        // $data = mb_convert_encoding($data, "ASCII");

        // print($data);

        $length = strlen($data);
        $ret = socket_send($socket, $data, $length, MSG_DONTROUTE); // Отправляем $length байт из $bindata
        
        // TO Получать ответ сокета
        $res = socket_close($socket); // Закрываем сокет

        echo($res);
	echo($ret);
    }

    $start["action"] = "status";
    $start["user"] = "vasia";
    $start["process"] = "ffmpeg_rtmp";
    $start["comand"] = "";

    // print_r($start);
    sendData($start)
?>
