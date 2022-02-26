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

  protected $template;
  protected $visitor_url;
  protected $order; // keeping track of what order should be passed when clicking header col of result table
  protected $toggle_expired;
  protected $toggle_expired_message;
  protected $search_string_brand_len;
  protected $search_string_article_len;

  function __construct () {
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/find/NavigationFind.php';
    require_once '../applications/find/TemplateFind.php';
    require_once '../applications/find/QueryFind.php';

    // html starts here
    $this->template = new TemplateFind();
    $this->template->start();

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

  protected function get_search_string_brand_len () {
    $this->search_string_brand_len = strlen($_GET['input_field_brand']);
  }

  protected function get_search_string_article_len () {
    $this->search_string_article_len = strlen($_GET['input_field_article']);
  }
}

class Home extends Find {
    public function run () {
      $navigation = new NavigationFind();
      $this->template->top_navbar($navigation->top_nav_links);
      $this->template->title('Søk etter vare');
      $this->template->print();
    }
}

class BySearch extends Find {
  public function run () {
    $title = 'Søk etter vare';
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");

    $navigation = new NavigationFind();
    $this->template->top_navbar($navigation->top_nav_links);

    $this->template->title($title);

    // preserving the previous brand and title search if passed, else empty
    $brand = '';
    $title = '';
    if(isset($_GET['input_field_brand'])) {
      $brand = $_GET['input_field_brand'];
    }
    if(isset($_GET['input_field_article'])) {
      $title = $_GET['input_field_article'];
    }
    $this->template->form_search($brand, $title);


    // if form is passed, handle query
    if(isset($_GET['input_field_brand']) or isset($_GET['input_field_article'])) {
      $this->result_set();
    }

    $this->template->print();
  }

  private function result_set () {
    // if search string is to short, the query will become to expensive
    // and potentially to many rows; we set a lower limit to characters
    $this->get_search_string_brand_len();
    $this->get_search_string_article_len();
    if ($this->search_string_brand_len < 1 and $this->search_string_article_len < 1) {
      return;
    }
    else if ($this->search_string_brand_len < 1 and $this->search_string_article_len < 5) {
      $this->template->message('Hvis du utelater Merke, bruk minst 5 tegn for å søke på artikkel');
      return;
    }
    else if ($this->search_string_article_len < 1 and $this->search_string_brand_len < 4) {
      $this->template->message('Hvis du utelater Artikkel, bruk minst 4 tegn for å søke på Merke');
      return;
    }
    else if (($this->search_string_brand_len + $this->search_string_article_len) < 4) {
      $this->template->message('Minst 5 tegn (fordelt på Merke og Artikkel) totalt for å søke');
      return;
    }

    $hyper_link_toggle = new HyperLink();
    $hyper_link_toggle->add_query('items', $this->toggle_expired);
    $this->template->hyperlink($this->toggle_expired_message, $hyper_link_toggle->url);
    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->table_start();
    $this->template->table_row_start();
    $hyper_link_header = new HyperLink();
    foreach ($table_headers as $alias => $name) {
      $hyper_link_header->add_query('sort', $name);
      $hyper_link_header->add_query('order', $this->order);
      $header_val = '<a href="' . $hyper_link_header->url . '">' . $alias . '</a>';
      $this->template->table_row_header($header_val);
    }
    $this->template->table_row_end();
    $query = new QueryFindBySearch();
    $query->where_brand();
    $query->where_article();
    $query->where_article_expired();
    $query->sort_by();

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
    $this->template->end();

  }
}

class ByBarcode extends Find {
  public function run () {
    echo 'This is Find->ByBarcide';
  }
}
