<?php

class Barcodes {

  protected $page = 'Strekkoder';
  protected $environment;
  protected $template;
  protected $navigation;
  protected $api_url;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/barcodes/TemplateBarcodes.php';
    require_once '../applications/barcodes/NavigationBarcodes.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationBarcodes();
    $this->template = new TemplateBarcodes();

    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

  protected function get_api_url () {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    $api_url = 'http://'.$host.':'.$port.'/';
  }

}


class Home extends Barcodes {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
  }

}


class GenerateLabels extends Barcodes {

  private $url_api;
  private $valid_barcodes;
  private $data_send;

  public function run () {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    $this->url_api = 'http://'.$host.':'.$port.'/';
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
      $this->load_label_form();
      $this->template->print();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      $api_endpoint = $this->url_api . 'shelf/';

      $this->validate_labels();
      if ($this->valid_barcodes) {
        $this->send_labels_to_api();
        return;
      }
      $this->load_label_form();
      $this->template->print();
    }
  }

  private function load_label_form () {
    // we fetch the N max amount of sheets and generate N form inputs
    $api_endpoint = $this->url_api . 'shelf/sheet/limit';
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $api_endpoint);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    if ($http_status_code === 200) {
      $response = json_decode($body, $associative = true);
      $sheet_limit = intval($response['limit']);
      $this->template->_label_form($sheet_limit);
      $hyperlink = new HyperLink();
      $this->template->hyperlink_button('Slett', $hyperlink->url);
    } else {
      $this->template->message('Ingen kontakt med: ' . $this->url_api);
    }
  }

  private function validate_labels () {
    $this->valid_barcodes = false;
    $this->data_send = [
      'barcodes' => array(),
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    foreach ($_POST as $key => $val) {
      if (preg_match('/(\ø|æ|å|Ø|Æ|Å)/', $val) ) {
        $this->template->message($val . ' inneholder ugyldig tegn');
        $this->valid_barcodes = false;
        return;
      }
      if ($val != '') {
        array_push ($this->data_send['barcodes'], $val);
        $this->valid_barcodes = true;
      }
    }
  }

  private function send_labels_to_api () {
    $api_endpoint = $this->url_api . 'shelf/';
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $api_endpoint);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($this->data_send));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    if (curl_errno($curl)) {
      if ( $this->environment->developement('show_debug') ) {
        echo 'http status code: ' . $http_status_code;
        die('Error on curl request: ' . curl_error($curl));
      }
    }
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
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
