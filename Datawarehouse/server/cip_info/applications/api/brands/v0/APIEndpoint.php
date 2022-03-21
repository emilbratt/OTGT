<?php

class APIEndpoint {

  protected $data;
  protected $request;
  protected $http_response_code;
  protected $valid_requests;

  function __construct ($request) {
    $this->request = $request;
  }

  public function run () {

  }

  public function get_data () {
    return $this->data;
  }

  public function get_return_code () {
    return $this->http_response_code;
  }


}
