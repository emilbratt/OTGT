<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $request;

  function __construct ($request) {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/api/article/v0/APIQueryRetail.php';
    $this->http_response_code = 404;
    $this->data = '';
    $this->request = $request;
  }

  public function run () {
    switch ($this->request[0]) {
      case 'get_article_id':
        $this->get_article_id();
        break;
      case 'movement':
        $this->movement();
        break;
      case 'sales':
        $this->data = ['response' => 'article sales not implemented yet'];
        $this->http_response_code = 404;
        break;
      case 'imports':
        $this->data = ['response' => 'article imports not implemented yet'];
        $this->http_response_code = 404;
        break;
      default:
        $this->data = ['response' => 'invalid endpoint'];
        $this->http_response_code = 500;
    }
  }

  private function get_article_id () {
    $this->data = ['articleid' => false];
    $this->http_response_code = 404;
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->data = ['response' => 'invalig method'];
      $this->http_response_code = 404;
      return;
    }
    if ( !(isset($this->request[1])) ) {
      $this->data = ['response' => 'no barcode was passed'];
      $this->http_response_code = 500;
      return;
    }
    if ( !(is_numeric($this->request[1])) ) {
      $this->data = ['response' => 'barcode should be numeric'];
      $this->http_response_code = 500;
      return;
    }

    $barcode = $this->request[1];
    $query = new APIQueryRetail();
    $query->get_article_id($barcode);
    $database_retail = new DatabaseRetail();
    $database_retail->select_single_row($query->get());
    $query = null;
    if ($database_retail->result) {
      $this->data = $database_retail->result;
      $this->http_response_code = 200;
    }
  }

  private function movement () {
    $this->data = ['response' => false];
    $this->http_response_code = 404;
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->data = '';
      $this->http_response_code = 404;
      return;
    }
    if ( !(isset($this->request[1])) ) {
      $this->http_response_code = 500;
      return;
    }
    if ( !(is_numeric($this->request[1])) ) {
      $this->http_response_code = 500;
      return;
    }

    $article_id = $this->request[1];
    $query = new APIQueryRetail();
    $query->movement($article_id);
    $database_retail = new DatabaseRetail();
    $database_retail->select_multi_row($query->get());
    $query = null;
    if ($database_retail->result) {
      $this->data = $database_retail->result;
      $this->http_response_code = 200;
    }
  }

}
