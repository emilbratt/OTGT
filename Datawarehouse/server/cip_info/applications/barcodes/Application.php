<?php

class Barcodes {

  protected $page = 'Strekkoder';
  protected $environment;
  protected $url_api;
  protected $template;
  protected $char_limit;
  protected $navigation;
  protected $label;
  protected $valid_label;
  protected $data_send;

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

  protected function get_api_url ($query = false) {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    if ( !($query)) {
      $this->url_api = 'http://'.$host.':'.$port.'/';
      return;
    }
    $this->url_api = 'http://'.$host.':'.$port.'/' . $query;
  }

  protected function validate_label () {
    $this->valid_label = false;
    if (preg_match('/(\ø|æ|å|Ø|Æ|Å)/', $this->label) ) {
      $this->template->message($this->label . ' inneholder ugyldig tegn');
      $this->valid_label = false;
      return;
    }
    if ( strlen($this->label) > $this->char_limit ) {
      $this->template->message($this->label . ' inneholder for mange tegn');
      $this->template->message('Max tegn: ' . strval($this->char_limit) );
      $this->valid_label = false;
      return;
    }
    if ($this->label != '') {
      $this->valid_label = true;
      return;
    }
  }

}


class Home extends Barcodes {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
  }

}


class GenerateBarcode extends Barcodes {

  public function run () {
    $hyperlink = new HyperLink();
    $hyperlink->link_redirect('barcodes');
    $this->template->hyperlink_button('Tilbake', $hyperlink->url);

    $this->char_limit = 100;
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    $this->load_form();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      $this->get_api_url('barcode/single/');
      $this->label = $_POST['form_input_label'];
      $this->validate_label();
      if ($this->valid_label) {
        $this->send_label_to_api();
      }
    }
    $this->template->print();
  }

  private function load_form () {
    $this->template->form_start('POST');
    $this->template->form_input_label('form_input_label', $focus = true);
    $this->template->form_end('Lag strekkode');
  }


  private function send_label_to_api () {
    $this->valid_label = false;
    $this->data_send = [
      'barcodes' => [$this->label],
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $this->url_api);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($this->data_send));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    if (curl_errno($curl)) {
      if ( $this->environment->developement('show_debug') ) {
        $this->template->message('Error on curl request: ' . curl_error($curl));
      }
      $this->template->message('Ingen kontakt med strekkode generator: ' . $this->url_api);
    }
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close ($curl);
    if ($http_status_code == 201) {
      $this->template->image_show($body);
    }
  }

}


class GenerateShelfLabels extends Barcodes {

  private $sheet_limit;
  private $limit_fetch_ok;

  public function run () {
    $hyperlink = new HyperLink();
    $hyperlink->link_redirect('barcodes');
    $this->template->hyperlink_button('Tilbake', $hyperlink->url);

    $this->valid_label = false;
    $this->get_api_url();
    $this->get_limits();
    $this->load_shelf_label_form();
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
      $this->template->print();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      $this->validate_labels();
      if ($this->valid_label) {
        // no html printing because we expect an octet stream (byte array)
        $this->send_labels_to_api();
        return;
      }
      $this->template->print();
    }
  }

  private function load_shelf_label_form () {
    if ($this->limit_fetch_ok) {
      $this->template->_shelf_label_form($this->sheet_limit, $this->char_limit);
      $hyperlink = new HyperLink();
      // center button and message with custom html
      $this->template->custom_html('<div class="center_div">');
      $this->template->custom_html('<br>');
      $this->template->hyperlink_button('Tøm alle felt', $hyperlink->url);
      $this->template->message('<br>Lag hyllemerker for å skrive ut på A4 ark');
      $this->template->custom_html('</div>');
    } else {
      if ( $this->environment->developement('show_debug') ) {
        $this->template->message('Could not establish contact with barcode_generator api');
        $this->template->message('On URL ' . $this->url_api);
      }
      $this->template->message('Ingen kontakt med strekkode generator: ' . $this->url_api);
    }
  }

  private function get_limits () {
    /**
     * the limits we need to know:
     *  1. how many labels can fit on an A4 sheet for printing
     *  2. how wide can the label be in regards of how many characters
     */

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
    $has_label = false;
    $this->data_send = [
      'barcodes' => array(),
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    foreach ($_POST as $key => $this->label) {
      $this->valid_label = false;
      if ($this->label == '') {
        // we allow empty label when creating multiple
        $this->valid_label = true;
      }
      else {
        $has_label = true;
        $this->validate_label();
        array_push ($this->data_send['barcodes'], $this->label);
        $this->valid_label = true;
      }
      if ( !($this->valid_label) ) {
        return;
      }
    }

    // if no labels pushed into array, just force invalid label
    if ( !($has_label) ) {
      $this->valid_label = false;
    }
  }

  private function send_labels_to_api () {
    $this->get_api_url('shelf/');
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $this->url_api);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($this->data_send));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    if (curl_errno($curl)) {
      if ( $this->environment->developement('show_debug') ) {
        $this->template->message('Error on curl request: ' . curl_error($curl));
        $this->template->print();
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
