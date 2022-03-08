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
 *  add. turnover report
 *  add. app to find items by name, brand, category, barcode etc..
 *  add. app to update shelf value
 *  add. batch update loction for items
 *  add. click on location in result and get map view
 *  add. create barcodes (python backend with python-barcode?)
 */

// temporary enable error reporting


require_once '../applications/AppRequest.php';
$main = new Apprequest;
$main = null;
