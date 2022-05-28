<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $fileobject;
  protected $request;

  function __construct ($request) {
    require_once '../applications/api/instructions/v0/APIObjectStorage.php';
    $this->request = $request;
    $this->data = array();
  }

  public function run () {
    $this->http_response_code = 500;
    switch ($this->request[0]) {
      case "view":
      $this->view();
        break;
      case "delete":
        $this->delete();
        break;
      case "create":
        $this->create();
        break;
      default:
        $this->data = ['response' => 'could not find endpoint'];
        $this->http_response_code = 404;
    }
  }

  private function view () {
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    // if less than 3, we do not have a full path to the file to be deleted
    if (count($this->request) < 3) {
      $this->data['response'] = 'add instruction to URL';
      return;
    }
    if (count($this->request) < 2) {
      $this->data['response'] = 'add category and instruction to URL';
      return;
    }
    $category = $this->request[1];
    $instruction = $this->request[2];
    $fileobject = new APIObjectStorage;
    if ( !($fileobject->set_path_file($category . '/' . $instruction)) ) {
      $this->data['response'] = $instruction . ' does not exist';
      $this->http_response_code = 404;
      return;
    }
    $abs_path = $fileobject->get_path_file();
    if ( $fileobject->read_file() ) {
      $this->http_response_code = 200;
    }
    $this->data['response'] = 'Error reading ' . $abs_path;
    $this->http_response_code = 500;
  }

  private function delete () {
    if ($_SERVER['REQUEST_METHOD'] !== 'DELETE') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    // if less than 3, we do not have a full path to the file to be deleted
    if (count($this->request) < 3) {
      $this->data['response'] = 'add instruction to URL';
      return;
    }
    if (count($this->request) < 2) {
      $this->data['response'] = 'add category and instruction to URL';
      return;
    }
    $category = $this->request[1];
    $instruction = $this->request[2];
    $fileobject = new APIObjectStorage;
    $fileobject->set_path_file($category . '/' . $instruction);
    $abs_path = $fileobject->get_path_file();
    if ($fileobject->delete_file() ) {
      $this->data['response'] = true;
      $this->data['deleted_file'] = $abs_path;
      $this->http_response_code = 200;
      return;
    }
    $this->data['response'] = false;
    $this->data['failed_deleted_file'] = $fileobject->message_error;
    return;
  }

  private function create () {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    $this->data['response'] = 'not implemented yet';
  }

}
