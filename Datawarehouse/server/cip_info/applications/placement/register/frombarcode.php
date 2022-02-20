<?php

class Page {

  private $query;
  private $cnxn;

  function __construct () {
    require_once './applications/Database.php';
    require_once './applications/Helpers.php';
    echo 'placement by barcode';
  }

}
