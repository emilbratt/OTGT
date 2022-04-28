<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $article_id;
  protected $shelf;
  protected $database_retail;
  protected $database_datawarehouse;
  protected $request;

  function __construct ($request) {
    require_once '../applications/api/placement/v0/APIQueryRetail.php';
    require_once '../applications/api/placement/v0/APIQueryDatawarehouse.php';
    $this->request = $request;
    $this->data = array();

    // return variables for response to caller to know if request was OK (true)
    $this->data['database_retail'] = false;
    $this->data['database_datawarehouse'] = false;
  }

  public function run () {
    switch ($this->request[0]) {
      case "update_by_article_id":
        $this->update_by_article_id();
        break;
      case "updatebybarcode":
        $this->updatebybarcode();
        break;
      default:
        $this->data = ['response' => 'invalid endpoint'];
        $this->http_response_code = 500;
    }
  }

  private function update_by_article_id () {
    $this->http_response_code = 500;
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      $this->http_response_code = 404;
      return;
    }
    if ( !(isset($_POST['article_id'])) ) {
      $this->data['response'] = 'missing key: article_id';
      return;
    }
    $this->article_id = $_POST['article_id'];
    if ( !(isset($_POST['shelf'])) ) {
      $this->data['response'] = 'missing key: shelf';
      return;
    }
    $this->shelf = $_POST['shelf'];

    // make sure article id is numeric
    if ( !(is_numeric($this->article_id)) ) {
      $this->data['response'] = 'article id should be numeric';
      return;
    }

    // make sure shelf has value
    if (strlen($this->shelf) < 1) {
      $this->data['response'] = 'shelf value is empty';
      return;
    }

    // format the shelf value by swapping + to -
    $this->shelf = str_replace('+', '-', $this->shelf);
    $this->shelf = strtoupper($this->shelf);
    // avoid whitespace values
    if ( (strlen($this->shelf) == 1) and ($this->shelf == ' ') ) {
      $this->data['response'] = 'shelf value invalid';
      return;
    }

    // only allow if "-" after first letter
    if (strlen($this->shelf) > 1) {
      if ( !(strpos($this->shelf, '-'))) {
        $this->data['response'] = 'shelf value ' .$this->shelf . ' invalid';
        return;
      }
    }

    $this->http_response_code = 201;
    $this->update_placement_to_retail();
    $this->insert_placement_to_datawarehouse();

  }

  private function update_placement_to_retail () {
    $query_retail = new APIQueryRetail();
    $database_retail = new DatabaseRetail();
    $query_retail->update_placement_by_article_id($this->article_id, $this->shelf);
    $stmt = $database_retail->cnxn->prepare($query_retail->get());
    try {
      $stmt->execute();
      $this->data['database_retail'] = true;
    }
    catch(PDOException $e) {
      $this->http_response_code = 502;
      $this->data['database_retail'] = false;
    }
  }

  private function insert_placement_to_datawarehouse () {
    $date_obj = new Date;
    $database_datawarehouse = new DatabaseDatawarehouse();
    $query_datawarehouse = new APIQueryDatawarehouse();

    $timestamp = $date_obj->date_time;
    $yyyymmdd = $date_obj->yyyymmdd;

    $query_datawarehouse->insert_placement();
    $stmt = $database_datawarehouse->cnxn->prepare($query_datawarehouse->get());

    $values = [
      'article_id' => $this->article_id,
      'shelf' => $this->shelf,
      'timestamp' => $timestamp,
      'yyyymmdd' => $yyyymmdd
    ];
    // since article_id constraint might not have been updated to datawareouse
    // we make a try / exception to handle that specific case
    try {
      $stmt->execute($values);
      $this->data['database_datawarehouse'] = true;
    }
    catch(PDOException $e)  {
      $this->data['database_datawarehouse'] = false;
      if (strpos($e, 'Integrity constraint violation') !== false) {
        $this->http_response_code = 502;
      }
      else {
        $this->http_response_code = 502;
      }
    }
  }

}
