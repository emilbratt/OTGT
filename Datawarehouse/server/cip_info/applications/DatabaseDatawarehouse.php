<?php

class DatabaseDatawarehouse {

  private $environment;
  public $cnxn;
  public $result;
  public $columns;
  public $rows;
  public $col_count;

  function __construct () {
    $this->environment = new Environment();
    $db_host = $this->environment->datawarehouse('db_host');
    $db_port = $this->environment->datawarehouse('db_port');
    $db_name = $this->environment->datawarehouse('db_name');
    $cnxn_str = "mysql:host=$db_host;dbname=$db_name;port=$db_port";
    $db_user = $this->environment->datawarehouse('db_user_post');
    $db_password = $this->environment->datawarehouse('db_password_post');
    try {
      $this->cnxn = new PDO($cnxn_str, $db_user, $db_password);
      $this->cnxn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    catch (Exception $e) {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo '</pre>';
      }
      else {
        echo '<pre>';
        echo 'Kontakt:';
        echo $this->environment->contact_dev('name') . '<br>';
        echo $this->environment->contact_dev('email') . '<br>';
        echo $this->environment->contact_dev('phone');
        echo '</pre>';
      }
      exit(1);
    }
  }

  public function select_single_row ($query) {
    try {
      $stmt = $this->cnxn->prepare($query);
      $stmt->execute();
      $this->result = $stmt->fetch(PDO::FETCH_ASSOC);
      $this->col_count = $stmt->columnCount();
    }
    catch(Exception $e)  {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
  }

  public function select_multi_row ($query) {
    try {
      $stmt = $this->cnxn->prepare($query);
      $stmt->execute();
      $this->result = $stmt->fetchAll(PDO::FETCH_ASSOC);
      $this->col_count = $stmt->columnCount();
    }
    catch(Exception $e)  {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }

  }

  function __destruct () {

  }

}
