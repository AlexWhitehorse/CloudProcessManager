<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);



    // Making querry string to the socket
    $user = $_GET["user"];
    $process = $_GET["process"];
    // $state = 'out';
    // $data = "{\"".$user."\": {\"".$process."\":{\"comand\":\"\",\"state\":\"".$state."\"}}}";
    $data =  "{\"procId\": \"".$user."/".$process."\",\"tsFrom\":\"".(time() + 2)."000000\"}";
    $length = strlen($data);
    // print_r($data);
    // --------------------------

    // $result = "";
    // $fileName = $user ."_". $process .".txt";
    // $_PATH_TO_LOGS = '../logs/'.$fileName;

    // $seconds = 0.5;

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

    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); // Создаем TCP Socket
    socket_bind($socket, 'localhost');
    $ret = socket_connect($socket, "localhost", 33334); // Устанавливаем соединение
    
    if(!$ret): print("error connecting"); die(); endif;

    $ret = socket_send($socket, $data, $length, MSG_DONTROUTE); // Отправляем $length байт из $bindata


    // $timeNow = date('U');
    

    // $fp = fopen($_PATH_TO_LOGS, 'w');
    $read = '';
    // passing unused strings
    for ($i=0; $i < 8; $i++) { 
        $read = $read . socket_read($socket, 1024,  PHP_NORMAL_READ);
        // print_r(socket_read($socket, 1024,  PHP_NORMAL_READ));
    }

    // $read = socket_read($socket, ,  PHP_NORMAL_READ);
    // $res = MakeNormStr($read);

    socket_close($socket);

    print_r($read);
?>