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
    require_once '../applications/api/APILog.php';
  }

  protected function parse_request_for_api () {
    /**
     * turns:
     *    query string: api/brands/v0/foo,bar/this/that
     * into:
     *   api_version: v0
     *   api_name: brands
     *   api_request: ['foo,bar', 'this', 'that']
     */
    $this->http_response_code = 204;
    // get the name that comes after api/
    $this->api_name = explode ('/', $_SERVER['REDIRECT_URL'], 4)[2];
    $delimiter = strtolower($this->api_name.'/');
     $endpoint = explode ($delimiter, $_SERVER['REDIRECT_URL'], 2)[1];
     $query_string = explode ('/', $endpoint, 2);

     // extract version number from query string
     $this->api_verison = $query_string[0];

     // extract request form query string as array separated by /
     $this->api_request = explode ('/', $query_string[1]);
     require_once "../applications/api/$this->api_name/$this->api_verison/APIEndpoint.php";
  }

  public function run () {
    // every api request is ran from here by inherited objects
    $this->parse_request_for_api();
    $api = new APIEndpoint($this->api_request);
    $api->run();
    $api_log = new APILog();
    $api_log->run();
    header('Content-Type: application/json; charset=utf-8');
    http_response_code($api->http_response_code);
    echo json_encode($api->data);
  }

}


class Home extends API {

 /**
  * only the home page should render a template while the
  * rest of the api application returns json objects
  *
  * this page is only meant to print out information
  * about the api endpoints that is available
  */

  protected $template;
  protected $navigation;
  protected $hyperlink;
  protected $current_api_endpoints;
  protected $formdata;

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
        ['url' => 'api/article/v0/movement/{article_id}', 'method' => 'GET', 'info' => 'get list of all movements for specific item', 'active' => true],
        ['url' => 'api/article/v0/get_article_id/{barcode}', 'method' => 'GET', 'info' => 'get article id from barcode', 'active' => true],
      ],
      'Placement' => [
        ['url' => 'api/placement/v0/update_by_article_id {"article_id": "val", "shelf": "val"}', 'method' => 'POST', 'info' => 'placement for item by article id', 'active' => true],
        ['url' => 'api/placement/v0/updatebybarcode {"barcode: "val", "shelf": "val"}', 'method' => 'POST', 'info' => 'placement for item by barcode', 'active' => false],
      ],
      'Shop' => [
        ['url' => 'api/shop/v0/howbusy/{N_seed_minutes})', 'method' => 'GET', 'info' => 'get integer 1-10 (1 relaxed to 10 busy) with {N} = include sales from N minutes back', 'active' => true],
      ],
      'Cache' => [
        ['url' => 'api/cache/v0/read/{key}', 'method' => 'GET', 'info' => 'get cache', 'active' => true],
        ['url' => 'api/cache/v0/set {"mem_key: "val", "mem_val": "val"}', 'method' => 'POST', 'info' => 'insert cache', 'active' => true],
        ['url' => 'api/cache/v0/delete/{key}', 'method' => 'DELETE', 'info' => 'delete cache', 'active' => true],
      ],
      // 'Brands' => [
      //   ['url' => 'api/brands/v0/all', 'method' => 'GET', 'info' => 'get list of all brands', 'active' => false],
      //   ['url' => 'api/brands/v0/brand/{brand_id}', 'method' => 'GET', 'info' => 'get info for specific brand', 'active' => false],
      // ],
      'Instructions' => [
        ['url' => 'api/instructions/v0/view/{category}/{instruction}.pdf', 'method' => 'GET', 'info' => 'view/download instruction', 'active' => true],
        ['url' => 'api/instructions/v0/create/ {""}', 'method' => 'POST', 'info' => 'add instruction (pdf)', 'active' => false],
        ['url' => 'api/instructions/v0/delete/{category}/{instruction}.pdf', 'method' => 'DELETE', 'info' => 'delete instruction', 'active' => true],
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
    $this->template->print($this->page);
  }

  protected function get_form_data_from_stream () {
    // creates a php array that can be accessed with $var['key']
    parse_str(file_get_contents("php://input"), $this->formdata);
  }

}

/**
 *
 * classes / pages that must be declared for the api endpoints
 * for that page to be reachable from the AppRequest.php script
 *
 */

class Barcode extends API {
  // get article data from barcode
}

class Cache extends API {
  // get, set and delete data from datwarehouse cache database table
}

class Brands extends API {
  // get details about brands
}

class Article extends API {
  // get article data from article id
}

class Placement extends API {
  // update item location
}

class Shop extends API {
  // variuos metrics and general data regarding retail shop
}

class Instructions extends API {
  // handle instructions (pdf files) with ObjectStorage class
}

class Test extends API {
  // simple test for checking your own connection/implementation
}
