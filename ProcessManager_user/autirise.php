<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

include_once 'ProcessManager.php';

// Если имя и пароль совпадают с прописанными, то сохраняет в кукм и
// перенаправляет на главную

    $login = $_POST['login'];
    $password = $_POST['password'];

    if($ret = getUserData($login, $password) ) 
    {
        print("sucscess <br>");
        setcookie("password", $password);
        setcookie("login", $login);

        print($ret['isAdmin']);

        if($ret['isAdmin'])
        {
            print("admin <br>");
            setcookie("isAdmin", "1");
        }
        else
        {
            print("Simple user <br>");
            setcookie("isAdmin", "0");
        }

        header("Location: index.php");
    }
    else{
        ?>
        <script type="text/javascript">
            alert("Не правильное имя пользователя или пароль")
            window.location.href = 'index.php';
        </script>
        <?php
        // header("Location: index.php");
    }
?>