<?php
// temporary enable error reporting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


require_once './applications/Request.php';
$main = new Apprequest;
$main = null;
// die;

// print out globals
echo '<pre>';
print_r($_SERVER);
print_r($_GET);
echo '</pre>';
