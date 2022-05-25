<?php

/**
 *
 * TODO:
 *  add turnover report
 *  add app find -> items by category
 *  add batch update placement for items
 */



// load the envirement for system wide configurations, auth. and settings
// that is used globally in the repository
const ENVIRONMENT_INI = '../../../../environment.ini';
// checking if environment.ini exists
if ( !(is_file(ENVIRONMENT_INI)) ) {
  echo 'create environment.ini from a copy of the environment.ini.template<br>';
  echo 'and fill in a value for each variable<br>';
  echo '<br>';
  echo 'the environment.ini should reside in the root of the repository<br>';
  echo 'i.e. the same directory as the environment.ini.template<br>';
  echo '<br>';
  echo 'script terminated';
  exit(1);
}
require_once '../applications/Environment.php';

 /**
  *
  * all requests regardless of URL or http method, goes through this file
  * which means that every dependent file that is included will have to
  * be referenced as of the relative path to THIS file
  *
  */

 /**
  * WARNING:
  * due to php ini settings being handeled in AppRequest.php,
  * ABSOLUTELY NO LOGIC should be added to this file
  *
  * this file should remain untouched as errors before loading
  * AppRequest.php wont be reported if this script fails
  */


// the main entrypoint
require_once '../applications/AppRequest.php';
$main = new Apprequest;
$main = null;
