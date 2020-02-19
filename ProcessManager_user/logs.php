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

$logName = false;

if( isset($_GET['process']) ){
    $logName = $_GET['process'];
}

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


<body>
    <header class="position-fixed container-fluid headerLine">
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="d-flex flex-row">

                        <!-- <a class="d-flex mr-auto stl-btns btn btn-secondary goBack" href="index.php">Назад</a> -->
                        <!-- <a href="mainPage.php">
                            <button type="button" 
                            class="d-flex mr-auto stl-btns btn btn-default buttons" 
                            id="Dirs" 
                            title="">
                                На главную
                            </button>
                        </a> -->
                        <div class="headerText_2 d-flex flex-grow-1 justify-content-center">
                            <?php
                                if($logName){
                                    echo('Log: ' . $logName);
                                }
                                else{
                                    echo('Не существует');
                                }
                            ?>                   
                        </div> 
                        <div class="controlPanel d-flex flex-row align-items-center">
                            
                            <button type="button" 
                            class="d-flex ml-auto stl-btns btn buttons border log-control-btn" 
                            id="scrolling"
                            style="margin-right: 2px;"
                            title="Остановить прокрутку"
                            >
                                <img class="color-svg" src="icons/triangle-down.svg" aria-hidden="true">
                            </button>

                            <button type="button" 
                            class="d-flex ml-auto stl-btns btn buttons border log-control-btn" 
                            id="update-logs"
                            title="Остановить обновление"
                            >
                                <img class="color-svg" src="icons/sync.svg" aria-hidden="true">
                            </button>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container" id="mainPage">
        <div class="row">
            <div class="col-sm-12">
                <!-- <pre id="outText"> -->
                    
                <!-- </pre> -->
                <div id="outText">

                </div>
            </div>
        </div>
    </div>




    <!-- Jquerry -->
    <script src="dependances/jquery-3.4.1.min.js" defer></script>
    <!-- My scripts -->
    <script src="scriptsJS/GetLogs.js" defer></script>
</body>


<?php
}
?>