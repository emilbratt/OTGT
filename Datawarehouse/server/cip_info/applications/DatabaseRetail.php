<?php

class DatabaseRetail {

  private $environment;
  public $cnxn;
  public $result;
  public $columns;
  public $rows;
  public $col_count;

  function __construct () {
    $this->environment = new Environment();
    $db_host = $this->environment->retail('db_host');
    $db_port = $this->environment->retail('db_port');
    $db_name = $this->environment->retail('db_name');
    $cnxn_str = "odbc:Driver=FreeTDS; Server=$db_host; Port=$db_port; Database=$db_name;";
    $db_user = $this->environment->retail('db_user');
    $db_password = $this->environment->retail('db_password');
    try {
      $this->cnxn = new PDO($cnxn_str, $db_user, $db_password);
      $this->cnxn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    catch (Exception $e)  {
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

  public function select_sinlge_row ($query) {
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
