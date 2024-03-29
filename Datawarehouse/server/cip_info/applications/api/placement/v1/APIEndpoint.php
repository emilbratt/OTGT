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
    require_once '../applications/api/placement/v1/APIQueryRetail.php';
    require_once '../applications/api/placement/v1/APIQueryDatawarehouse.php';
    $this->http_response_code = 500;
    $this->request = $request;
    $this->data = array();

    // default value for response and changes only on success
    $this->data['database_retail'] = false;
    $this->data['database_datawarehouse'] = false;
  }

  public function run () {
    switch ($this->request[0]) {
      case 'update_by_article_id':
        $this->update_by_article_id();
        break;
      default:
        $this->data = ['response' => 'could not find endpoint'];
        $this->http_response_code = 404;
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
      $this->http_response_code = 501;
      $this->data['response'] = 'missing key: article_id';
      return;
    }
    $this->article_id = $_POST['article_id'];
    if ( !(isset($_POST['shelf'])) ) {
      $this->http_response_code = 501;
      $this->data['response'] = 'missing key: shelf';
      return;
    }
    $this->shelf = $_POST['shelf'];

    // make sure article id is numeric
    if ( !(is_numeric($this->article_id)) ) {
      $this->http_response_code = 501;
      $this->data['response'] = 'article id should be numeric';
      return;
    }

    // make sure shelf has value
    if (strlen($this->shelf) < 1) {
      $this->http_response_code = 501;
      $this->data['response'] = 'shelf value is empty';
      return;
    }

    // make sure shelf value is not to long
    if (strlen($this->shelf) > 9) {
      $this->http_response_code = 501;
      $this->data['response'] = 'shelf value to long';
      return;
    }

    // avoid an empty whitespace value
    if ( (strlen($this->shelf) == 1) and ($this->shelf == ' ') ) {
      $this->http_response_code = 501;
      $this->data['response'] = 'shelf value is an empty whitespace';
      return;
    }

    // swap out de-limitters to "-" (currently allow "+", " ", and ".")
    $this->shelf = str_replace('+', '-', $this->shelf);
    $this->shelf = str_replace(' ', '-', $this->shelf);
    $this->shelf = str_replace('.', '-', $this->shelf);
    $this->shelf = str_replace(',', '-', $this->shelf);
    $this->shelf = strtoupper($this->shelf);

    // only allow if "-" in string if longer than 1 character
    if (strlen($this->shelf) > 1) {
      if ( !(strpos($this->shelf, '-')) ) {
        $this->http_response_code = 501;
        $this->data['response'] = 'shelf value ' . $this->shelf . ' has no delimitter';
        return;
      }
    }

    $this->http_response_code = 201;
    $this->placement_to_retail();
    $this->placement_to_datawarehouse();
    $this->data['response'] = true;
  }

  private function placement_to_retail () {
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

  private function placement_to_datawarehouse () {
    $db_datawarehouse = new DatabaseDatawarehouse();
    $query = new APIQueryDatawarehouse();

    $date_obj = new Date;
    $values = [
      'article_id' => $this->article_id,
      'shelf' => $this->shelf,
      'timestamp' => $date_obj->date_time,
      'yyyymmdd' => $date_obj->yyyymmdd
    ];

    // first, try to do an update of timestamp (works if placement exists)
    $query->update_timestamp_for_placement();
    $stmt = $db_datawarehouse->cnxn->prepare($query->get());
    // we make a try / exception to handle error
    try {
      $stmt->execute($values);
      $this->data['database_datawarehouse'] = true;
      if ($stmt->rowCount() > 0) {
        // affected rows means record exists and timestamp update succeeded
        return;
      }
    }
    catch(PDOException $e) {
      $this->data['database_datawarehouse'] = false;
      $this->http_response_code = 502;
      return;
    }

    // if this block runs, it means we need to insert a new record
    $query->insert_placement();
    $stmt = $db_datawarehouse->cnxn->prepare($query->get());
    // we make a try / exception to handle error
    try {
      $stmt->execute($values);
      $this->data['database_datawarehouse'] = true;
      return;
    }
    catch(PDOException $e) {
      $this->data['database_datawarehouse'] = false;
      $this->http_response_code = 502;
      return;
    }
  }

}
