<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $request;
  protected $database_retail;
  protected $database_dw;

  function __construct ($request) {
    require_once '../applications/api/sales/v0/APIQueryRetail.php';
    // require_once '../applications/api/sales/v0/APIQueryDatawarehouse.php';
    $this->request = $request;
    $this->http_response_code = 500;
    $this->data = array();
  }

  public function run () {
    // set default response for now
    switch ($this->request[0]) {
      case 'salesperhour':
        $this->salesperhour();
        break;
      default:
        $this->data = ['response' => 'could not find endpoint'];
        $this->http_response_code = 404;
    }
  }

  private function salesperhour () {
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    if (count($this->request) == 4) {
      $year = $this->request[1];
      $month = $this->request[2];
      $day = $this->request[3];
    }
    if (count($this->request) == 3) {
      $year = $this->request[1];
      $month = $this->request[2];
      $day = 0;
    }
    if (count($this->request) == 2) {
      $year = $this->request[1];
      $month = 0;
      $day = 0;
    }
    if (count($this->request) < 2) {
      $this->data['response'] = 'add at least year to URL';
      return;
    }
    // month and day is set to 0 because we check for numerical value
    if ( !(is_numeric($year)) or !(is_numeric($month)) or !(is_numeric($day)) ) {
      $this->data['response'] = 'parameters can only be integers';
      return;
    }
    $query = new APIQueryRetail();
    $this->database_retail = new DatabaseRetail();
    $query->salesperhour($year, $month, $day);
    $this->database_retail->select_multi_row($query->get());
    if ( !($this->database_retail->result) ) {
      $this->http_response_code = 204;  // 204 = no content
      return;
    }
    $this->data = $this->database_retail->result;
    $this->http_response_code = 200;

  }

}
