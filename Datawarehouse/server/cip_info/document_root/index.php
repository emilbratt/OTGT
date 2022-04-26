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

// the environment file as seen relative from this directory
const FILE_ENVIRONMENT = '../../../../environment.ini';
// and checking if it is created on a new installation
if ( !(is_file(FILE_ENVIRONMENT)) ) {
  echo 'create environment.ini from a copy of the environment.ini.template<br>';
  echo 'and fill in a value for each variable<br>';
  echo '<br>';
  echo 'the environment.ini should reside in the root of the repository<br>';
  echo 'i.e. the same directory as the environment.ini.template<br>';
  echo '<br>';
  echo 'script terminated';
  exit(1);
}

require_once '../applications/AppRequest.php';
$main = new Apprequest;
$main = null;
