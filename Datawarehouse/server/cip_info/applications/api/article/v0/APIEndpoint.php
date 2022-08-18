<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $request;
  protected $article_id;
  protected $adjustment_id;
  protected $days_back;

  function __construct ($request) {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/api/article/v0/APIQueryRetail.php';
    require_once '../applications/api/article/v0/APIQueryDatawarehouse.php';
    $this->http_response_code = 500;
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
      case 'sales_count':
        $this->sales_count();
        break;
      case 'imports':
        $this->data = ['response' => 'article imports not implemented yet'];
        $this->http_response_code = 500;
        break;
      default:
        $this->data = ['response' => 'could not find endpoint'];
        $this->http_response_code = 404;
    }
  }

  private function get_article_id () {
    $this->data = ['articleid' => false];
    $this->http_response_code = 404;
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->http_response_code = 405;
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
      $this->http_response_code = 405;
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

  private function sales_count () {
    $this->data = ['response' => false];
    $this->http_response_code = 404;
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->http_response_code = 405;
      return;
    }
    if ( !(isset($this->request[1])) ) {
      $this->http_response_code = 500;
      return;
    }
    if ( !(is_numeric($this->request[1])) ) {
      $this->data = ['response' => 'only numeric values allowed'];
      $this->http_response_code = 500;
      return;
    }
    $this->article_id = $this->request[1];
    $this->adjustment_id = '0';
    if ( count($this->request) == 3 ) {
      if ( !(is_numeric($this->request[2])) ) {
        $this->data = ['response' => 'only numeric values allowed'];
        $this->http_response_code = 500;
        return;
      }
      $this->days_back = $this->request[2];
      $this->get_min_stock_adjustment_id_by_days_back();
    }
    if ( $this->adjustment_id === false ) {
      $this->data = ['response' => 'could not get adjustment_id, this might be bacause no article movement has occured today'];
      $this->http_response_code = 500;
      return;
    }
    $database_retail = new DatabaseRetail();
    $query_retail = new APIQueryRetail();
    // if id from cache was not found or if id not valid, we need to grab from retail database
    $query_retail->sales_count($this->article_id, $this->adjustment_id);
    // $query_retail->print();
    $database_retail->select_single_row($query_retail->get());
    // insert to cache if row returned
    if ($database_retail->result) {
      $this->data['response'] = true;
      $this->data['sales_count'] = $database_retail->result['sales_count'];
      $this->http_response_code = 200;
    }
  }

  private function get_min_stock_adjustment_id_by_days_back () {
    $database_dw = new DatabaseDatawarehouse();
    // format days back to yyyymmdd and use as mem_key
    $string_minus_days = '-' . $this->days_back . ' day';
    $yyyymmdd = date('Y_m_d', strtotime($string_minus_days));
    $mem_key = 'api_article_v0_min_stock_adjustment_id_for_' . $yyyymmdd;
    // fetch value from cache table
    $database_dw->mem_delete_yesterday($mem_key);
    if ( isset($database_dw->mem_get($mem_key)['mem_val']) ) {
      $this->adjustment_id = $database_dw->mem_get($mem_key)['mem_val'];
      if ( is_numeric($this->adjustment_id) ) {
        // this means we got a "valid" value from cache table and can return
        return;
      }
    }
    // if id from cache was not found or if its not valid, we need to grab new
    $database_retail = new DatabaseRetail();
    $query_retail = new APIQueryRetail();
    $query_retail->min_stock_adjustment_id_for_day_back($this->days_back, );
    $database_retail->select_single_row($query_retail->get());
    $val = $database_retail->result['stock_adjustment_id'];
    if ($database_retail->result) {
      $this->adjustment_id = $database_retail->result['stock_adjustment_id'];
      $database_dw->mem_insert($mem_key, $this->adjustment_id);
      return;
    }
    $this->adjustment_id = false;
  }

}
