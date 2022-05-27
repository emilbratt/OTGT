<?php

require_once '../applications/ObjectStorage.php';

class APIObjectStorage extends ObjectStorage {

  function __construct () {
    parent::__construct();
    $this->set_root_path('instructions');
  }

}
