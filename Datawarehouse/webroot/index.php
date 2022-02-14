<?php
// temporary enable error reporting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


require_once './applications/controller.php';
$request = new Controller;


// remove the ugly signature that mess up the print_r on $_SERVER
$_SERVER['SERVER_SIGNATURE'] = '';
// print out globals
echo '<pre>';
print_r($_SERVER);
print_r($_GET);
echo '</pre>';
