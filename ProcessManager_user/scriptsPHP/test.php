<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

// var_dump(time());
var_dump(microtime(true));
$user = 123;
$process = 2222;

print("{\"procId\": \"".$user."/".$process."\",\"tsFrom\":\"".(time() + 2)."000000\"}");

?>