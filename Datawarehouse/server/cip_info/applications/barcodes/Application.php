<?php

class Barcodes {

  protected $page = 'Strekkoder';
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/barcodes/TemplateBarcodes.php';
    require_once '../applications/barcodes/NavigationBarcodes.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationBarcodes();
    $this->template = new TemplateBarcodes();

    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Barcodes {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
  }

}


class GenerateShelfLabels extends Barcodes {

  public function run () {
    // just a working proof of concept for now, will change this
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_internal_port');
    $query = 'shelf/';
    $url = 'http://'.$host.':'.$port.'/'.$query;
    $data = [
      'barcodes' => [
        "A-A-1", "A-A-2", "A-A-3", "A-A-4", "A-A-5", "A-A-6",
        "A-A-7", "A-A-8", "A-A-9", "A-A-10", "A-A-11", "A-A-12",
        "A-A-13", "A-A-14", "A-A-15", "A-A-16", "A-A-17", "A-A-18",
        "A-A-19", "A-A-20", "A-A-21", "A-A-22", "A-A-23", "A-A-24",
        "A-A-25", "A-A-26", "A-A-27", "A-A-28", "A-A-29", "A-A-30",
        "A-A-31", "A-A-32", "A-A-33", "A-A-34", "A-A-35", "A-A-36",
      ],
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    if (curl_errno($curl)) {
      if ( $this->environment->developement('show_debug') ) {
        echo 'http status code: ' . $http_status_code;
        die('Error on curl request: ' . curl_error($curl));
      }
    }
    curl_close ($curl);
    if ($http_status_code == 201) {
      header('Content-Type: image/png');
      header('Content-Type: application/octet-stream');
      header('Content-Transfer-Encoding: binary');
      header('Content-Disposition: attachment; filename=strekkoder.png');
      echo $body;
    }
  }
}
