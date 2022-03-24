<?php

class APIEndpoint {

  protected $data;
  protected $request;
  protected $http_response_code;

  function __construct ($request) {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/api/article/v0/APIQueryRetail.php';
    $this->http_response_code = 404;
    $this->data = '';
    $this->request = $request;
  }

  public function run () {
    switch ($this->request[0]) {
      case 'movement':
        $this->movement();
        break;
      case 'sales':
        echo 'article sales not implemented'; die;
        break;
      case 'imports':
        echo 'article imports not implemented'; die;
        break;
    }
  }

  public function get_data () {
    return $this->data;
  }

  public function get_return_code () {
    return $this->http_response_code;
  }

  private function movement () {
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
    $query->article_movement($article_id);
    $database_retail = new DatabaseRetail();
    $database_retail->select_multi_row($query->get());
    $query = null;
    if ($database_retail->result) {
      $this->data = $database_retail->result;
      $this->http_response_code = 200;
    }
  }

}
