<?php

require_once '../applications/ObjectStorage.php';

class APIObjectStorage extends ObjectStorage {

  function __construct () {
    parent::__construct();
    $this->set_root_path('instructions');
  }

  public function read_file () {
    // disable error messages to avoid otherwise it will mess up json response
    ini_set('display_errors', 0);
    try {
      header('Content-Type: application/pdf');
      header("Content-Disposition: inline; filename='$this->name_file'");
      readfile($this->path_file);
    }
    catch (Exception $e) {
      return false;
    }
  }


}
