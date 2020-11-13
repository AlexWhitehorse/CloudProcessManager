<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);



    // Making querry string to the socket
    $user = $_GET["user"];
    $process = $_GET["process"];
    $state = 'out';
    // $data = "{\"".$user."\": {\"".$process."\": {\"comand\": \"[]\", \"state\": \"".$state."\"}}}";
    $data = "{\"procId\": \"".$user."/".$process."\",\"tsFrom\":\"".(time() - 20)."000000\"}";
    $length = strlen($data);
    // --------------------------

    $result = "";
    $fileName = $user ."_". $process .".txt";
    $_PATH_TO_LOGS = '../logs/'.$fileName;

    $seconds = 60;


    // Преобразование строки из сокета в необходимый формат
    function MakeNormStr($str)
    {
        $pos=strrpos($str, "frame=");
        $res=substr($str, $pos);

        if (strrpos($str, "frame=") > 1 ){
            return $res . '<br>';
        }
        if (strpos($str, '(copy)')){
            return '';
        }

        return $str . '<br>';
    }
    //$initTime = Текущее время с начала века
    function timer($sec, $initTime)
    {
        $deadline = $initTime + $sec;
        $nowTime = date('U');

        if ($deadline > $nowTime) {
            return true;
        }
        else return false;
    }

    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // Создаем TCP Socket
    socket_bind($socket, 'localhost');
    $ret = socket_connect($socket, "localhost", 33334); // Устанавливаем соединение
    
    if(!$ret): print("Error connecting"); die(); endif;

    $ret = socket_send($socket, $data, $length, MSG_DONTROUTE); // Отправляем $length байт из $bindata


    $timeNow = date('U');
    

    $fp = fopen($_PATH_TO_LOGS, 'w');

    // passing unused strings
    for ($i=0; $i < 8; $i++) { 
        socket_read($socket, 1024,  PHP_NORMAL_READ);
    }

    while (timer($seconds, $timeNow)) {

        $read = socket_read($socket, 1024,  PHP_NORMAL_READ);
        $res = MakeNormStr($read);

        fwrite($fp, $res);
    }

    // Закрываем сокет и удаляем файл
    fclose($fp);
    socket_close($socket); 

    unlink($_PATH_TO_LOGS);




?>