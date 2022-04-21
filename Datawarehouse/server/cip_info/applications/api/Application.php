<?php

class API {

  protected $page = 'API';
  protected $data;
  protected $api_name;
  protected $api_endpoint;
  protected $api_request;
  protected $environment;
  protected $http_method;
  protected $api_verison;
  protected $http_response_code;

  function __construct () {
    require_once '../applications/Date.php';
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
  }

  protected function parse_request_for_api () {
    $this->http_response_code = 204;

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

  protected function log_request () {
    if ($this->http_response_code >= 200 and $this->http_response_code <= 299) {
      header('Content-Type: application/json; charset=utf-8');
      echo json_encode($this->data);
    }
  }

  protected function send_json () {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($this->data);
    http_response_code($this->http_response_code);
  }


  public function run () {
    // every api request is ran from here by inherited objects
    $this->parse_request_for_api();
    $api = new APIEndpoint($this->api_request);
    $api->run();
    $this->data = $api->data;
    $this->http_response_code = $api->http_response_code;
    $this->send_json();
  }

}


class Home extends API {

 /**
  * only the home page should render a template
  * while the rest of the api app serves json
  *
  * this page is only meant to print out information
  * about the api endpoints that exists
  */

  protected $template;
  protected $navigation;
  protected $hyperlink;
  protected $current_api_endpoints;

  function __construct () {
    require_once '../applications/HyperLink.php';
    require_once '../applications/api/NavigationAPI.php';
    require_once '../applications/api/TemplateAPI.php';

    $this->hyperlink = new HyperLink();
    $this->template = new TemplateAPI();
    $this->navigation = new NavigationAPI();

    // update this list as new api endponts are added
    $this->current_api_endpoints = [
      'Test' => [
        ['url' => 'api/test/v0/hello', 'method' => 'GET', 'info' => 'request hello to get dummy data', 'active' => true],
        ['url' => 'api/test/v0/hello', 'method' => 'POST', 'info' => 'request hello and get back the post data you sent', 'active' => true],
        ['url' => 'api/test/v0/foo', 'method' => 'GET', 'info' => 'request foo to get dummy data', 'active' => true],
      ],
      'Article' => [
        ['url' => 'api/article/v0/movement/{article_id}', 'method' => 'GET', 'info' => 'get list of all movements for specific item', 'active' => false],
      ],
      'Placement' => [
        ['url' => 'api/placement/v0/update_by_article_id {"article_id": "val", "shelf": "val"}', 'method' => 'POST', 'info' => 'placement for item by article id', 'active' => true],
        ['url' => 'api/placement/v0/updatebybarcode {"barcode: "val", "shelf": "val"}', 'method' => 'POST', 'info' => 'placement for item by barcode', 'active' => false],
      ],
      'Brands' => [
        ['url' => 'api/brands/v0/all', 'method' => 'GET', 'info' => 'get list of all brands', 'active' => false],
        ['url' => 'api/brands/v0/brand/{brand_id}', 'method' => 'GET', 'info' => 'get info for specific brand', 'active' => false],
      ],
    ];
  }

  public function run () {
    $this->hyperlink->link_redirect();
    $home = $this->hyperlink->url;
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
    $this->template->title('Api Endpoints');
    foreach ( $this->current_api_endpoints as $endpoint => $desc ) {
      $this->template->endpoint_title($endpoint);
      $this->template->table_start();
      foreach ($desc as $row ) {
        if ($row['active']) {
          $this->template->table_row_start();
          $this->template->table_row_value($row['method']);
          $this->template->table_row_value($row['url']);
          $this->template->table_row_value($row['info']);
          $this->template->table_row_end();
        }
      }
      $this->template->table_end();
    }
    $this->template->print();
  }

}

/**
 *
 * classes / pages that must be declared for the api endpoints to be reachable
 *
 */

class Brands extends API {

}

class Article extends API {

}

class Placement extends API {

}

class Test extends API {

}
