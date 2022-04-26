<?php

/**
 *
 * TODO:
 *  add turnover report
 *  add app find -> items by category
 *  add batch update placement for items
 */

 /**
  * all requests regardles of URL or http method, goes through this file
  * which means that every dependent file that is included will have to
  * be referenced as of the relative path to THIS file
  *
  */


require_once '../applications/AppRequest.php';
$main = new Apprequest;
$main = null;
