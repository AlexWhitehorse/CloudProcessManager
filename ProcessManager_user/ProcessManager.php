<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);



function getUserData($userName, $password){
    $data = parse_ini_file("processes.ini", true, INI_SCANNER_RAW);

    foreach ($data as $key => $value){

        if(isAdmin($key, $value, $userName, $password) )
        {
            // print_r("Admin");
            return ["isAdmin" => true, 'data' => $data];
            // exit;
            // break;
        }

        if($ret = isUser($key, $value, $userName, $password))
        {
            // print_r("User");
            return ["isAdmin" => false, 'data' => $ret];
            // exit;
            // break;
        }
    };

    return false;

}


function isAdmin($key, $arr, $userName, $pass)
{

    $name = $arr["name"];
    $password = $arr["password"];

    if($key == "admin" & $name == $userName & $password == $pass){

        if($name == $userName & $password == $pass){
            return true;
        }
        return 0;
    }
}


function isUser($key, $arr, $userName, $pass)
{
    if($key == $userName & $arr["password"] == $pass){
        return array(
            $userName => array(
                "name" => $userName,
                "alias" => $arr['name'],
                "processes" => $arr["processes"]
            )
        );
        // return true;
    }
}


// print_r( json_encode( getUserData("admin", "123") ));
// print("</br>");
// print_r( json_encode( getUserData($ini_array, "vasia", "1234") ))
?>