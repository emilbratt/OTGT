<?php
/**
 * all requests regardles of URL or http method, goes through this file
 * this means that every dependent file that is included will have to
 * be referenced as of the relative path to THIS file
 *
 * keeping in mind this is not a REST-API, but rather a front-and-back-end
 * baked into each other forming the application where each app directory is
 * one specific service
 *
 * TODO:
 *  add. js for handeling search filter of result set
 *  add. turnover report
 *  add. app to find items by name, brand, category, barcode etc..
 *  add. app to update shelf value mobile and desktop freindly
 */

// temporary enable error reporting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);



require_once '../applications/Request.php';
$main = new Apprequest;
$main = null;
// die;

// print out globals
echo '<pre>';
print_r($_SERVER);
print_r($_GET);
echo '</pre>';
