<?php

class APIEndpoint {

  public $data;
  public $http_response_code;
  protected $request;
  protected $database_retail;
  protected $database_dw;
  protected $min_customer_sales_id_today;
  protected $seed_minutes;
  protected $howbusy_result;
  protected $n_sales;
  protected $n_sellers;
  protected $description;
  const HOW_BUSY_HEX_COLOUR_CODE = [
    '0' => '#C4EFFF',
    '1' => '#C4EFFF',
    '2' => '#A2F2DD',
    '3' => '#ABF5CC',
    '4' => '#9BF2B4',
    '5' => '#96FA99',
    '6' => '#ADFF85',
    '7' => '#DEFF7A',
    '8' => '#FF7C17',
    '9' => '#FF4B0A',
    '10' => '#ED0000',
  ];
  const HOW_BUSY_RGB_COLOUR_CODE = [
    '0' => '196, 239, 255',
    '1' => '196, 239, 255',
    '2' => '162, 242, 221',
    '3' => '171, 245, 204',
    '4' => '155, 242, 180',
    '5' => '150, 250, 153',
    '6' => '173, 255, 133',
    '7' => '222, 255, 122',
    '8' => '255, 124, 23',
    '9' => '255, 75, 10',
    '10' => '237, 0, 0',
  ];
  const HOW_BUSY_DESCRIPTION = [
    '0' => 'Ingen pågang',
    '1' => 'Veldig lite pågang',
    '2' => 'Noe pågang',
    '3' => 'Merkbar Pågang',
    '4' => 'En del pågang',
    '5' => 'Mye pågang',
    '6' => 'Mye pågang',
    '7' => 'Mye pågang',
    '8' => 'Veldig mye pågang',
    '9' => 'Veldig mye pågang',
    '10' => 'Veldig mye pågang',
  ];
  const HOW_BUSY_PERCENTAGE = [
    '0' => '0%',
    '1' => '10%',
    '2' => '20%',
    '3' => '30%',
    '4' => '40%',
    '5' => '50%',
    '6' => '60%',
    '7' => '70%',
    '8' => '80%',
    '9' => '90%',
    '10' => '100%',
  ];

  function __construct ($request) {
    require_once '../applications/api/shop/v0/APIQueryRetail.php';
    require_once '../applications/api/shop/v0/APIQueryDatawarehouse.php';
    $this->request = $request;
    $this->http_response_code = 500;
    $this->data = array();
  }

  public function run () {
    // set default response for now
    switch ($this->request[0]) {
      case 'howbusy':
        $this->howbusy();
        break;
      default:
        $this->data = ['response' => 'could not find endpoint'];
        $this->http_response_code = 404;
    }
  }

  private function howbusy () {
    if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
      $this->data['response'] = 'invalid method: ' . $_SERVER['REQUEST_METHOD'];
      return;
    }
    if (count($this->request) < 2) {
      $this->data['response'] = 'add number of minutes as seed to URL';
      return;
    }
    $this->seed_minutes = $this->request[1];
    if ( !(is_numeric($this->seed_minutes)) ) {
      $this->data['response'] = $this->seed_minutes . ' is not a number';
      return;
    }
    $this->database_retail = new DatabaseRetail();
    $this->get_min_customer_sales_id_today();
    $this->calculate_how_busy();
    $this->data['result'] = $this->howbusy_result;
    $this->data['desc'] = self::HOW_BUSY_DESCRIPTION[$this->howbusy_result];
    $this->data['hex'] = self::HOW_BUSY_HEX_COLOUR_CODE[$this->howbusy_result];
    $this->data['rgb'] = self::HOW_BUSY_RGB_COLOUR_CODE[$this->howbusy_result];
    $this->data['precent'] = self::HOW_BUSY_PERCENTAGE[$this->howbusy_result];
    $this->data['sales'] = $this->n_sales;
    $this->data['sellers'] = $this->n_sellers;
    $this->http_response_code = 200;

  }

  private function get_min_customer_sales_id_today () {
    $database_dw = new DatabaseDatawarehouse();
    $database_dw->mem_delete_yesterday('min_customer_sales_id_today');
    // the end result of this block will either pass a number or just false to min_customer_sales_id_today
    $min_id = $database_dw->mem_get('min_customer_sales_id_today')['mem_val'];
    if ($min_id != false) {
      // we might still have grabbed yesterdays id from cache
      // if inserted at around 00:00 on date shift (this has happened)
      // lets really confirm that this id is todays minimum sales id
      $query_retail = new APIQueryRetail();
      $query_retail->select_confirm_min_customer_sales_id_is_today($min_id);
      $this->database_retail->select_single_row($query_retail->get());
      $is_valid = $this->database_retail->result['min_id'];
      // if row returned, id is valid and we can jump out
      if ($is_valid) {
        $this->min_customer_sales_id_today = $min_id;
        return;
      }
      unset($query_retait);
    }

    $query_retail = new APIQueryRetail();
    // if id from cache was not found or if id not valid, we need to grab from retail database
    $query_retail->select_min_customer_sales_id_today();
    $this->database_retail->select_single_row($query_retail->get());
    // if row returned, we have an id and can update cache
    $this->min_customer_sales_id_today = $this->database_retail->result['min_id'];
    // insert to cache if row returned
    if ($this->min_customer_sales_id_today) {
      $database_dw->mem_insert('min_customer_sales_id_today', $this->min_customer_sales_id_today);
      return;
    }
  }

  private function calculate_how_busy () {
    // if we hav min_customer_sales_id_today, we can qoery for how busy
    if ($this->min_customer_sales_id_today) {
      $query = new APIQueryRetail();
      $query->howbusy($this->seed_minutes, $this->min_customer_sales_id_today);
      $this->database_retail->select_single_row($query->get());
      if ($this->database_retail->result != false) {
        // grouping by seller means that we will get a row for each seller
        $this->howbusy_result = strval($this->database_retail->result['busy_result']);
        $this->n_sales = strval($this->database_retail->result['sales']);
        $this->n_sellers = strval($this->database_retail->result['sellers']);
        return;
      }
    }
    // no results = no sales => not busy
    $this->howbusy_result = '0';
    $this->n_sales = '0';
    $this->n_sellers = '0';
  }
}
