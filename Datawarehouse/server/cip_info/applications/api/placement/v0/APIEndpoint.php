<?php

class APIEndpoint {

  protected $data;
  protected $article_id;
  protected $shelf;
  protected $request;
  protected $http_response_code;

  function __construct ($request) {
    require_once '../applications/Date.php';
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/api/article/v0/APIQueryRetail.php';
    $this->http_response_code = 404;
    $this->data = '';
    $this->request = $request;
  }

  public function run () {
    switch ($this->request[0]) {
      case "update_by_article_id":
        $this->update_by_article_id();
        break;
      case "update_by_barcode":
        $this->update_by_barcode();
        break;
    }
  }

  public function get_data () {
    return $this->data;
  }

  public function get_return_code () {
    return $this->http_response_code;
  }

  private function update_by_article_id () {
    $this->http_response_code = 500;


    // if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    //   $this->data = '';
    //   $this->http_response_code = 404;
    //   return;
    // }
    //
    // if ( !(isset($this->request[1])) ) {
    //   return;
    // }
    // if ( !(isset($this->request[2])) ) {
    //   return;
    // }
    //
    // $this->article_id = $this->request[1];
    // $this->shelf = $this->request[2];
    //
    // // make sure article id is numeric
    // if ( !(is_numeric($this->request[1])) ) {
    //   return;
    // }
    //
    // // make sure shelf has value
    // if (strlen($this->shelf) < 1) {
    //   $this->shelf = false;
    //   return;
    // }
    // // format the shelf value by swapping + to -
    // $this->shelf = str_replace('+', '-', $this->shelf);
    // $this->shelf = strtoupper($this->shelf);
    // // avoid whitespace values
    // if ( (strlen($this->shelf) == 1) and ($this->shelf == ' ') ) {
    //   $this->shelf = false;
    //   return;
    // }
    //
    // // expect "-" after first letter
    // if (strlen($this->shelf) > 1) {
    //   if ( !(strpos($this->shelf, '-'))) {
    //     $this->shelf = false;
    //     return;
    //   }
    // }

    $this->http_response_code = 200;
    $this->data = ['HALT HERE'];
    return;

    $this->update_placement_to_retail();
    $this->insert_placement_to_datawarehouse();
    $this->http_response_code = 204;
  }

  private function update_placement_to_retail () {
    $query_retail = new APIQueryRetail();
    $database_retail = new DatabaseRetail();
    $query_retail->update_placement_by_article_id($this->article_id, $this->shelf);
    $stmt = $database_retail->cnxn->prepare($query_retail->get());
    $stmt->execute();
  }

  private function insert_placement_to_datawarehouse () {
    $date_obj = new Date;
    $query_datawarehouse = new QueryDatawarehousePlacement();
    $database_datawarehouse = new DatabaseDatawarehouse();

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
    }
    catch(PDOException $e)  {
      if (strpos($e, 'Integrity constraint violation') !== false) {
        $this->http_response_code = 502;
      }
      else {
        $this->http_response_code = 502;
      }
    }
  }

}
