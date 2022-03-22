<?php

class APIEndpoint {

  protected $data;
  protected $request;
  protected $http_response_code;
  protected $valid_requests;
  protected $dummy_data;

  function __construct ($request) {
    $this->http_response_code = 500;
    $this->data = '';

    $this->request = $request;
    $this->valid_requests = [
      'hello',
      'foo',
    ];

    $this->dummy_data = [
      'foo' => 'bar',
      'hello' => 'wrold',
    ];
  }

  public function run () {
    if ( !(in_array($this->request[0], $this->valid_requests)) ) {
      $this->http_response_code = 404;
      return;
    }
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
      $this->data = $this->dummy_data[$this->request[0]];
      $this->http_response_code = 200;
      return;
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      $this->data = $_POST;
      $this->http_response_code = 200;
      return;
    }

  }

  public function get_data () {
    return $this->data;
  }

  public function get_return_code () {
    return $this->http_response_code;
  }


}
