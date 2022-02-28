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
 *  add. app to update shelf value (mobile and desktop freindly)
 *  add. click on location in result and get map view (make svg image over floor plan)
 *  add. show last imported items and feature for updateing location
 *  add. batch update loction for items
 *  add. create barcodes (python backend with python-barcode?)
 */

// temporary enable error reporting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once '../applications/AppRequest.php';
$main = new Apprequest;
$main = null;
