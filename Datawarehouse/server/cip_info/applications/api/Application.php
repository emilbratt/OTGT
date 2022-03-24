<?php

class API {

  protected $page = 'Api';
  protected $api_name;
  protected $api_endpoint;
  protected $api_request;
  protected $environment;
  protected $http_method;
  protected $api_verison;
  protected $data;
  protected $http_response_code;


  protected function handle_api_request () {
    $this->http_response_code = 500;
    // get the name that comes after api/
    $this->api_name = explode ('/', $_SERVER['REDIRECT_URL'], 4)[2];
    $delimiter = strtolower($this->api_name.'/');
    /*
     * turns:
     *    REDIRECT URL: api/brands/v0/foo,bar/this/that
     * into:
     *   api_version: v0
     *   api_name: brands
     *   api_request: ['foo,bar', 'this', 'that']
     */
     $endpoint = explode ($delimiter, $_SERVER['REDIRECT_URL'], 2)[1];
     $query_string = explode ('/', $endpoint, 2);
     // extract version number from query string
     $this->api_verison = $query_string[0];
     // extract request form query string as array separated by /
     $this->api_request = explode ('/', $query_string[1]);
     require_once "../applications/api/$this->api_name/$this->api_verison/APIEndpoint.php";
  }

  protected function send_json () {
    if ($this->http_response_code === 200) {
      header('Content-Type: application/json; charset=utf-8');
      echo json_encode($this->data);
    }
    http_response_code($this->http_response_code);
  }

}


class Home extends API {

 /**
  * only the home page should render a template
  * while the rest of the api app serves json
  *
  * this page iso nly meant to print out information
  * about the api endpoints that exists
  */
  protected $template;
  protected $navigation;
  protected $current_api_endpoints;

  function __construct () {
    require_once '../applications/HyperLink.php';
    require_once '../applications/api/NavigationAPI.php';
    require_once '../applications/api/TemplateAPI.php';

    $this->template = new TemplateAPI();
    $this->navigation = new NavigationAPI();

    // update this list as new api endponts are added
    $this->current_api_endpoints = [
      'Test' => [
        ['url' => 'api/test/v0/hello', 'method' => 'GET', 'info' => 'request hello to get dummy data'],
        ['url' => 'api/test/v0/hello', 'method' => 'POST', 'info' => 'request hello and get back the post data you sent'],
         ['url' => 'api/test/v0/foo', 'method' => 'GET', 'info' => 'request foo to get dummy data'],
       ],
      'Placement' => [
         ['url' => 'api/placement/v0/placement{article_id},{location}', 'method' => 'PUT', 'info' => 'update placement for item'],
       ],
      'Article' => [
         ['url' => 'api/article/v0/article_movement', 'method' => 'GET', 'info' => 'get list of all movements for specific item'],
       ],
      'Brands' => [
         ['url' => 'api/brands/v0/all', 'method' => 'GET', 'info' => 'get list of all brands'],
         ['url' => 'api/brands/v0/brand/{brand_id}', 'method' => 'GET', 'info' => 'get info for specific brand'],
       ],
    ];
  }

  public function run () {
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
    $this->template->title('Api Endpoints');

    foreach ( $this->current_api_endpoints as $endpoint => $desc ) {
      $this->template->endpoint_title($endpoint);
      $this->template->table_start();
      foreach ($desc as $row ) {
        $this->template->table_row_start();
        $this->template->table_row_value($row['method']);
        $this->template->table_row_value($row['url']);
        $this->template->table_row_value($row['info']);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
    $this->template->print();
  }

}


class Brands extends API {

  public function run () {
    $this->handle_api_request();
    $api = new APIEndpoint($this->api_request);
    $api->run();
    $this->data = $api->get_data();
    $this->http_response_code = $api->get_return_code();
    $this->send_json();
  }

}


class Article extends API {

  public function run () {
    $this->handle_api_request();
    $api = new APIEndpoint($this->api_request);
    $api->run();
    $this->data = $api->get_data();
    $this->http_response_code = $api->get_return_code();
    $this->send_json();
  }

}

class Test extends API {

  public function run () {
    $this->handle_api_request();
    $api = new APIEndpoint($this->api_request);
    $api->run();
    $this->data = $api->get_data();
    $this->http_response_code = $api->get_return_code();
    $this->send_json();
  }

}
