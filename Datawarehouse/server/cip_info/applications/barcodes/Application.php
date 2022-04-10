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
  private $sheet_limit;
  private $char_limit;
  private $limit_fetch_ok;
  private $valid_labels;
  private $data_send;

  public function run () {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    $this->url_api = 'http://'.$host.':'.$port.'/';
    $this->get_limits();
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
      $this->load_label_form();
      $this->template->print();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      $api_endpoint = $this->url_api . 'shelf/';
      $this->validate_labels();
      if ($this->valid_labels) {
        // no html printing because we epect an image as octet stream (byte array)
        $this->send_labels_to_api();
        return;
      }
      $this->load_label_form();
      $this->template->print();
    }
  }

  private function load_label_form () {
    if ($this->limit_fetch_ok) {

      $this->template->_label_form($this->sheet_limit, $this->char_limit);

      $hyperlink = new HyperLink();
      // center button and message with custom html
      $this->template->custom_html('<div class="center_div">');
      $this->template->custom_html('<br>');
      $this->template->hyperlink_button('Tøm alle felt', $hyperlink->url);
      $this->template->message('<br>Lag hyllemerker for å skrive ut på A4 ark');
      $this->template->custom_html('</div>');
    } else {
      if ( $this->environment->developement('show_debug') ) {
        echo 'Could not establish contact with barcode_generator api';
        echo 'On URL' . $this->url_api;
        die('Error on curl request: ' . curl_error($curl));
      }
      $this->template->message('Ingen kontakt med strekkode generator: ' . $this->url_api);
    }
  }

  private function get_limits () {
    // we fetch the N max amount of sheets and label chars generate N form inputs
    $api_sheet_limit = $this->url_api . 'shelf/sheet/limit';
    $api_char_limit = $this->url_api . 'shelf/char/limit';

    // build the individual requests, but do not execute them
    $curl_1 = curl_init($api_sheet_limit);
    $curl_2 = curl_init($api_char_limit);
    curl_setopt($curl_1, CURLOPT_URL, $api_sheet_limit);
    curl_setopt($curl_2, CURLOPT_URL, $api_char_limit);
    curl_setopt($curl_1, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl_2, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl_1, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl_2, CURLOPT_RETURNTRANSFER, true);

    // multi-curl handle for asynchronous fetching
    $mh = curl_multi_init();
    curl_multi_add_handle($mh, $curl_1);
    curl_multi_add_handle($mh, $curl_2);
    do {
        $status = curl_multi_exec($mh, $active);
        if ($active) {
            curl_multi_select($mh);
        }
    } while ($active && $status == CURLM_OK);
    curl_multi_remove_handle($mh, $curl_1);
    curl_multi_remove_handle($mh, $curl_2);
    curl_multi_close($mh);

    $this->sheet_limit = curl_multi_getcontent($curl_1);
    $this->sheet_limit = json_decode($this->sheet_limit, $associative = true);
    $this->char_limit = curl_multi_getcontent($curl_2);
    $this->char_limit = json_decode($this->char_limit, $associative = true);
    if (isset($this->sheet_limit['limit']) && isset($this->char_limit['limit'])) {
      $this->sheet_limit = $this->sheet_limit['limit'];
      $this->char_limit = $this->char_limit['limit'];
      $this->limit_fetch_ok = true;
    }
    else {
      $this->limit_fetch_ok = false;
    }
  }

  private function validate_labels () {
    // var_dump( $this->char_limit); die;
    $this->valid_labels = false;
    $this->data_send = [
      'barcodes' => array(),
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    foreach ($_POST as $key => $val) {
      if (preg_match('/(\ø|æ|å|Ø|Æ|Å)/', $val) ) {
        $this->template->message($val . ' inneholder ugyldig tegn');
        $this->valid_labels = false;
        return;
      }
      if ( strlen($val) > $this->char_limit ) {
        $this->template->message($val . ' inneholder for mange tegn');
        $this->template->message('Max tegn: ' . strval($this->char_limit) );
        $this->valid_labels = false;
        return;
      }
      if ($val != '') {
        array_push ($this->data_send['barcodes'], $val);
        $this->valid_labels = true;
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
