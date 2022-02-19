<?php
/**
 * this is not a REST-API, but rather a back-end and front-end baked into
 * this app directory for a simple way to interact with the shops database
 * providing easy access to reports and other features
 */

// temporary enable error reporting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


require_once './applications/Request.php';
$main = new Apprequest;
$main = null;
die;

// print out globals
echo '<pre>';
print_r($_SERVER);
print_r($_GET);
echo '</pre>';
