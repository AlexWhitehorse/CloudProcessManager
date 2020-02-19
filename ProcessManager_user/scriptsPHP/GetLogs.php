<?php
    ini_set('error_reporting', E_ALL);
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);

    include_once '../config.php';

    $file = "/var/www/html/ProcessManager_tmp/" . $_GET['user'] . "_" . $_GET['process'] . ".txt";

    if (file_exists($file)) 
    {
        $str = "tail -c ".NUM_OF_BITS_LOG." $file";

        $test = exec($str . ' 2>&1', $output);
        
        $data = explode("\r", $output[count($output) - 1]);

        $logOf['log'] = $data;

        $data = json_encode($logOf['log']);

    } else {
        $logOf['log'] = json_encode(false);

        $data = json_encode($logOf['log']);
    }

    print_r($data);

?>
