<?php

/**
 *
 * for finding items in a convenient fashion
 * searching by brand, article, barcode, category etc,
 *
 * TODO:
 *  add: all queries that have user-input should be logged
 *  add: click on result row to open detailed info about article
 *  add: check if image location exists to avoid throwing image not found error
 */

class Find {

  protected $page = 'Vare'; // alias for top_navbar
  protected $template;
  protected $navigation;
  protected $visitor_url;
  protected $sort_by; // keeping track of what column is sorted by
  protected $order; // keeping track of what order should be passed when clicking header col of result table
  protected $arrow_symbol; // show arrow pointing at the way the table is ordered
  protected $toggle_expired;
  protected $toggle_expired_message;
  protected $search_string_brand_len;
  protected $search_string_article_len;
  protected $search_string_barcode;

  function __construct () {
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/find/NavigationFind.php';
    require_once '../applications/find/TemplateFind.php';
    require_once '../applications/find/QueryFind.php';

    $this->template = new TemplateFind();
    $this->navigation = new NavigationFind();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);

    // default is ascending, but we flip the order of rows if ascending is already set
    $this->order = 'ascending';
    $this->arrow_symbol = ' &#8595;';
    if (isset($_GET['order'])) {
      if ($_GET['order'] == 'ascending') {
        $this->order = 'descending';
        $this->arrow_symbol = ' &#8593;';
      }
    }

    // default is ascending, but we flip the order of rows if ascending is already set
    $this->sort_by = null;
    if (isset($_GET['sort'])) {
      $this->sort_by = $_GET['sort'];
    }

    // default is none-expired (show only active articles), can be flipped with button
    $this->toggle_expired = 'active';
    $this->toggle_expired_message = 'Vis Kun Aktive';
    if(isset($_GET['items'])) {
      if($_GET['items'] == 'expired') {
        $this->toggle_expired = 'all';
        $this->toggle_expired_message = 'Vis Aktive & Utgåtte';
      }
      else if($_GET['items'] == 'active') {
        $this->toggle_expired = 'expired';
        $this->toggle_expired_message = 'Vis Kun Utgåtte';
      }
    }
  }

  protected function get_search_string_brand_len () {
    $this->search_string_brand_len = strlen($_GET['input_field_brand']);
  }

  protected function get_search_string_article_len () {
    $this->search_string_article_len = strlen($_GET['input_field_article']);
  }

  protected function validate_search_string_barcode () {
    $check_num = is_numeric($_GET['input_field_barcode']);
    $check_len = (strlen($_GET['input_field_barcode']) == 13 or strlen($_GET['input_field_barcode']) >= 8);
    $this->search_string_barcode = ($check_num == true and $check_len == true);
  }
}


class Home extends Find {

    public function run () {
      $this->template->sub_navbar($this->navigation->sub_nav_links);
      $this->template->print();
    }
}


class BySearch extends Find {

  public function run () {
    // preserving the previous brand and title search if passed, else empty
    if(isset($_GET['input_field_brand']) and isset($_GET['input_field_article'])) {
      $this->template->form_search($_GET['input_field_brand'], $_GET['input_field_article']);
    }
    else {
      $this->template->form_search();
    }

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
      return; // clicking search with both search boxes empty, just return (it might be a miss-click)
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

    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('items', $this->toggle_expired);

    $query = new QueryFindBySearch();
    $query->where_brand();
    $query->where_article();
    $query->where_article_expired();
    $query->sort_by();

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->hyperlink_button($this->toggle_expired_message, $hyperlink_toggle->url);
    $this->template->script_filter_row_button();

    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    foreach ($table_headers as $alias => $name) {
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    $this->template->table_row_end();

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
      $this->template->table_end();
      $this->template->css_by_search();
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

  }
}


class ByBarcode extends Find {
  public function run () {
    // preserving the previous brand and title search if passed, else empty
    if(isset($_GET['input_field_barcode'])) {
      $this->template->form_barcode($_GET['input_field_barcode']);
    }
    else {
      $this->template->form_barcode();
    }


    // if form is passed, handle query
    if(isset($_GET['input_field_barcode'])) {
      $this->result_set();
    }

    $this->template->print();
  }

  private function result_set () {
    // if search string is to short, the query will become to expensive
    // and potentially to many rows; we set a lower limit to characters
    $this->validate_search_string_barcode();
    if ( !($this->search_string_barcode) ) {
      return; // could not validate that a barcode as input
    }

    $query = new QueryFindByBarcode();
    $query->where_barcode();

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Kategori' => 'category',
      'Pris' => 'price',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Sist Importert' => 'lastimported',
      'Sist Solgt' => 'lastsold',
      // 'Lev. ID' => 'supplyid',
    ];



    $this->cnxn = Database::get_retail_connection();

    try {
      $sth = $this->cnxn->prepare($query->get());
      $sth->execute();
      $result = $sth->fetch(PDO::FETCH_ASSOC);
      if (!($result)) {$this->template->message('Ingen Treff'); return;}
      $this->template->table_full_width_start();
      $this->template->table_row_start();
      foreach ($table_headers as $alias => $name) {
        $this->template->table_row_value($alias);
      }
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['brand']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['article']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['category']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['price']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['quantity']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['location']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['lastimported']));
      $this->template->table_row_value(CharacterConvert::utf_to_norwegian($result['lastsold']));
      $this->template->table_row_end();
      $this->template->table_end();
      $this->template->css_by_barcode();

      if($result['location'] == null) {
        $this->template->image_location('empty');
        return;
      }
      $this->template->image_location($result['location']);
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
  }

}
