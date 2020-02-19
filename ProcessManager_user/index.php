<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

include_once 'ProcessManager.php';

// $cookiePass = isset($_COOKIE['password']);
// $cookieLogin = isset($_COOKIE['login']);

if (isset($_COOKIE['password']) & isset($_COOKIE['login'])): 
    $cookiePass = $_COOKIE['password'];
    $cookieLogin = $_COOKIE['login'];
else:
    $cookiePass = 0;
    $cookieLogin = 0;
endif;

if( ! getUserData($cookieLogin, $cookiePass))
{
    
    include_once 'pageLogining.html';

}
else if($userData = getUserData($cookieLogin, $cookiePass))
{

?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Process Manager</title>

    <link rel="text/plain" href="dependances/bootstrap-4.3.1-dist/css/bootstrap.css.map">
    <link rel="stylesheet" href="dependances/bootstrap-4.3.1-dist/css/bootstrap.css">
    <link rel="stylesheet" href="styles/index.css">
</head>

<body id="body">

    <header class="position-fixed container-fluid headerLine">
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="d-flex flex-row">

                        <img class="img-logo" src="icons/Easycaster_logo3_little.png" alt="" sizes="" srcset="">

                        <div class="headerText_2 d-flex flex-grow-1 justify-content-center">
                            Process Manager
                        </div>

                        <!-- Logout -->
                        <a href="Logout.php" style="margin-left:10px;">  
                            <button type="button"
                                class="logout d-flex ml-auto stl-btns btn buttons border">
                                    <img class="color-svg" src="icons/sign-out.svg" aria-hidden="true">
                            </button>
                        </a>

                    </div>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container header">
        <div class="row" id="content">
        

            </div>
    </div>
    









<?php

$user = $userData['data'];
$isAdmin = $userData['isAdmin'];
$json = json_encode($user);

// print_r($json);

$jsScript = "
    <script type=\"text/javascript\">
        // var initDataJson = {}
        var initDataJson = $json
        var isAdmin = \"$isAdmin\"
    </script>  
";
print($jsScript);

?>
    <script src="dependances/jquery-3.4.1.min.js" defer></script>
    <script src="scriptsJS/showUsers.js" defer></script>
</body>
</html>


<?php
}
//-- version 1.0 /ProcessManager was originally written by Alex Bielokone <sasha.belokone@gmail.com>
?>