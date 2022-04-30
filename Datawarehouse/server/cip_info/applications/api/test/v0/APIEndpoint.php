<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $request;
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
      'hello' => 'world',
    ];
  }

  public function run () {
    if ( !(in_array($this->request[0], $this->valid_requests)) ) {
      $this->http_response_code = 404;
      return;
    }
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
      // return they value that corresponds to the request query
      // e.g. test/v0/hello -> world, test/v0/foo -> bar
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
