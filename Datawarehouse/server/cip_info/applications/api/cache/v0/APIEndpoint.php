<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $database_datawarehouse;
  protected $request;
  protected $key;
  protected $value;

  function __construct ($request) {
    $this->request = $request;
    $this->http_response_code = 500;
    $this->data = array();
    $date_obj = new Date;
    $this->database_datawarehouse = new DatabaseDatawarehouse();
  }

  public function run () {
    // set default response for now
    $this->data['response'] = false;
    switch ($this->request[0]) {
      case 'read':
        $this->read();
        break;
      case 'set':
        $this->set();
        break;
      case 'delete':
        $this->delete();
        break;
      default:
        $this->data = ['response' => 'could not find endpoint'];
        $this->http_response_code = 404;
    }
  }

  private function read () {
    // this api endpoint expects a key to point to the value in the cache table
    if (count($this->request) < 2) {
      $this->data['response'] = 'need to add key parameter in URL';
      return;
    }
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    $this->key = $this->request[1];
    $val = $this->database_datawarehouse->mem_get($this->key);
    // key val pair for mem_val and mem_time returned if exists
    if ($val) {
      $this->data = $val;
      $this->http_response_code = 200;
      return;
    }
    // key not in cache database
    $this->http_response_code = 404;
    $this->data['response'] = $this->key . ' has no value';
  }

  private function set () {
    // this endpoint expects the key and value pair as form data
    $this->data['response'] = false;
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    if ( isset($_POST['mem_key']) and isset($_POST['mem_val']) ) {
      $this->key = $_POST['mem_key'];
      $this->value = $_POST['mem_val'];
      if ( $this->database_datawarehouse->mem_insert($this->key, $this->value) ) {
        $this->data['response'] = true;
        $this->http_response_code = 201;
        return;
      }
    }
    $this->data['response'] = false;
  }

  private function delete () {
    // this api endpoint expects a key to point to the value in the cache table
    if (count($this->request) < 2) {
      $this->data['response'] = 'need to add key parameter in URL';
      return;
    }
    if ($_SERVER['REQUEST_METHOD'] !== 'DELETE') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    $this->key = $this->request[1];
    $res = $this->database_datawarehouse->mem_delete($this->key);
    if ($res) {
      $this->data['response'] = $this->key . ' was deleted';
      $this->http_response_code = 200;
      return;
    }
    // key not in cache database
    $this->http_response_code = 404;
    $this->data['response'] = $this->key . ' has no value';
  }

}
