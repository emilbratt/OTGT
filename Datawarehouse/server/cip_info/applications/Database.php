<?php

class Database {

  public static function get_connection () {
    $config_file = '../../../../environment.ini';
    $config = parse_ini_file($config_file, $process_sections = true);

    $db_server = $config['retail']['db_server'];
    $db_port = $config['retail']['db_port'];
    $db_user = $config['retail']['db_user'];
    $db_password = $config['retail']['db_password'];
    $db_name = $config['retail']['db_name'];

    $connection_string = "odbc:Driver=FreeTDS; Server=$db_server; Port=$db_port; Database=$db_name;";

    try {
      $cnxn = new PDO($connection_string,  $db_user, $db_password);
      $cnxn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      return $cnxn;
    }
    catch(Exception $e)  {
      echo '<pre>';
      print_r($e->getMessage());
      echo '</pre>';
      exit(1);
    }
  }

}
