<?php

require_once '../applications/ObjectStorage.php';

class ObjectStorageInstructions extends ObjectStorage {

  public $upload_error;

  function __construct () {
    parent::__construct();
    $this->set_root_path('instructions');
  }

  public function upload_file ($key) {
    // will create a category folder set in path_current
    // and upload the designated file to this location

    $this->name_file = $_FILES[$key]['name'];
    $this->path_file = $this->path_current . '/' . $this->name_file;

    $this->normalize_path_file();
    if ( !(move_uploaded_file($_FILES[$key]["tmp_name"], $this->path_file)) ) {
      $this->message_error = 'FEIL: noe galt skjedde under lagring av ' . $this->name_file;
      $this->upload_error = true;
      return;
    }

    $this->message_ok = 'link til ' . $this->name_file;
    $this->upload_error = false;
    chmod($this->path_file, 0777);
  }

  public function read_file () {
    $this->path_file = $this->path_current . $this->name_file;
    $this->normalize_path_file();
    header('Content-Type: application/pdf');
    header("Content-Disposition: inline; filename='$this->name_file'");
    readfile($this->path_file);
  }

}
