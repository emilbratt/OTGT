<?php

/**
 *
 * for finding items in a convenient fashion
 * searching by brand, article, barcode, category etc,
 *
 * TODO:
 *  add: all queries that have user-input should be logged
 *  add: click on result row to open detailed info about article
 */

class Find {

  protected $visitor_url;
  protected $order;
  protected $toggle_expired;
  protected $toggle_expired_message;
  // protected $hyper_link_header;
  protected $template;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/find/TemplateFind.php';
    require_once '../applications/find/QueryFind.php';

    // default is ascending, but we flip the order of rows if ascending is already set
    $this->order = 'ascending';
    if (isset($_GET['order'])) {
      if ($_GET['order'] == 'ascending') {
        $this->order = 'descending';
      }
    }

    // default is none-expired (show only active articles), can be flipped with button
    $this->toggle_expired = 'all';
    $this->toggle_expired_message = 'Vis Aktive & Utgåtte';
    if(isset($_GET['items'])) {
      if($_GET['items'] == 'active') {
        $this->toggle_expired = 'expired';
        $this->toggle_expired_message = 'Vis Kun Utgåtte';
      }
      else if($_GET['items'] == 'all') {
        $this->toggle_expired = 'active';
        $this->toggle_expired_message = 'Vis Kun Aktive';
      }
    }

  }

  protected function check_minimum_search_string_brand () {
    // a short search string set to at least 2 characters for brand and
    // 3 characters for article will skip search
    // this is to avoid to large result-sets from the database query
    if(strlen($_GET['input_field_brand']) < 2) {
      return false;
    }
    return true;
  }

  protected function check_minimum_search_string_article () {
    // a short search string set to at least 2 characters for brand and
    // 3 characters for article will skip search
    // this is to avoid to large result-sets from the database query
    if(strlen($_GET['input_field_article']) < 3) {
      return false;
    }
    return true;
  }
}

class Home extends Find {

    public function run () {
      echo 'This is Find';
    }
}

class BySearch extends Find {
  public function run () {

    $title = 'Søk etter vare';
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");


    // html starts here
    $this->template = new TemplateFind();
    $this->template->start();
    $this->template->title($title);
    $brand = '';
    $title = '';
    if(isset($_GET['input_field_brand'])) {
      $brand = $_GET['input_field_brand'];
    }
    if(isset($_GET['input_field_article'])) {
      $title = $_GET['input_field_article'];
    }
    $this->template->form_search($brand, $title);
    $hyper_link_toggle = new HyperLink();
    $hyper_link_toggle->add_query('items', $this->toggle_expired);
    $this->template->hyperlink($this->toggle_expired_message, $hyper_link_toggle->url);

    if(isset($_GET['input_field_brand']) and isset($_GET['input_field_article'])) {
      $this->result_set();
    }

    $this->template->print();
  }

  private function result_set () {

    // if search string is to short, the query will become to expensive
    // and or have to many rows, we set a lower limit to characters
    if($_GET['input_field_brand'] == '') {
      $this->template->message('Minst 2 tegn for å søke på merke');
      return;
    }
    if($_GET['input_field_article'] == '') {
      return;
    }
    if(!($this->check_minimum_search_string_brand())) {
      $this->template->message('Minst 2 tegn for å søke på merke');
      return;
    }
    if(!($this->check_minimum_search_string_article())) {
      $this->template->message('Minst 3 tegn for å søke på Artikkel');
      return;
    }

    $table_headers = [
      ['Merke', 'brand'],
      ['Navn', 'article'],
      ['Lager', 'quantity'],
      ['Plassering', 'location'],
      ['Lev. ID', 'supplyid'],
    ];

    $this->template->table_start();
    $this->template->table_row_start();
    $hyper_link_header = new HyperLink();
    $hyper_link_header->link_home('hei', 'sann');
    foreach ($table_headers as $header) {
      $hyper_link_header->add_query('sort', $header[1]);
      $hyper_link_header->add_query('order', $this->order);
      $header_val = '<a href="' . $hyper_link_header->url . '">' . $header[0] .'</a>';
      $this->template->table_row_header($header_val);
    }
    $this->template->table_row_end();
    $query = new QueryFindBySearch();
    $query->add_search_brand();
    $query->add_search_article();
    $query->add_toggle_expired();
    $query->add_sort();
    $query->add_order();
    // $query->print_query();

    $this->cnxn = Database::get_retail_connection();

    try {
      foreach ($this->cnxn->query($query->get()) as $row) {
        $article = $row['articleid'];
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['supplyid']));
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      $config_file = '../../../../environment.ini';
      $config = parse_ini_file($config_file, $process_sections = true);
      if($config['developement']['show_errors']) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();
    $this->template->end();

  }
}

class ByBarcode extends Find {
  public function run () {
    echo 'This is Find->ByBarcide';
  }
}
