<?php

/**
 *
 * for finding items in a convenient fashion
 * searching by brand, article, barcode, category etc,
 *
 * TODO:
 *  add: all queries that have user-input should be logged
 *
 *    BySearch
 *      add: app "BySearch" click on result row to open detailed info about article
 *
 *    ByBarcode:
 *      fix: layout for table
 *      add: show shelf history
 *      add: show extended info from scanbybarcode
 */

class Find {

  protected $page = 'Finn Vare'; // alias for top_navbar
  protected $template;
  protected $environment;
  protected $database_retail;
  protected $database_datawarehouse;
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
  protected $search_string_article_id;

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/find/NavigationFind.php';
    require_once '../applications/find/TemplateFind.php';
    require_once '../applications/find/QueryRetailFind.php';
    require_once '../applications/find/QueryDatawarehouseFind.php';

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
  protected function validate_search_string_article_id () {
    $this->search_string_article_id = is_numeric($_GET['article_id']);
  }
}


class Home extends Find {

    public function run () {
      $this->template->sub_navbar($this->navigation->sub_nav_links);
      $this->template->print();
    }

}


class BySearch extends Find {

  /*
   * this page will list a result table based on kewords for article name and
   * brand name passed by the user
   */

  public function run () {
    $this->environment = new Environment();

    // preserving the previous brand and title search if passed, else empty
    $this->template->form_search();

    // if form is passed, handle query and show result table
    if(isset($_GET['input_field_brand']) or isset($_GET['input_field_article'])) {
      $this->result_set();
    }

    $this->template->css_by_search();
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

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Lev. ID & Strekkode' => 'supplyid',
    ];

    $this->template->hyperlink_button($this->toggle_expired_message, $hyperlink_toggle->url);
    $hyperlink_toggle = null;
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

    $query = new QueryRetailFindBySearch();
    $query->select_items_by_search();
    $query->where_brand();
    $query->where_article();
    $query->where_article_expired();
    $query->sort_by();
    $this->database_retail = new DatabaseRetail();
    $this->database_retail->select_multi_row($query->get());
    $query = null;
    if ($this->database_retail->result) {
      $hyperlink_row = new HyperLink();
      foreach ($this->database_retail->result as $row) {
        $article_id = $row['article_id'];
        $barcode = $row['barcode'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']), $hyperlink_row->url);
        $this->template->table_row_value($row['quantity']);
        $this->template->table_row_value($row['location'], $hyperlink_row->url);
        $this->template->table_row_value($row['supplyid'] . ' // ' . $barcode);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

}


class ByArticle extends Find {

  /*
   * this page will find one item either by barcode or by article_id
   */

  public function run () {
    $this->environment = new Environment();

    $this->template->form_barcode();

    // if form is passed or get request with article id, handle request
    if ( isset($_GET['input_field_barcode']) or isset($_GET['article_id']) ) {
      $this->result_set();
    }

    $this->template->print();
  }

  private function result_set () {

    if ( isset($_GET['input_field_barcode']) ) {
      $this->validate_search_string_barcode();
      if ( !($this->search_string_barcode) ) {
        $this->template->message('Ugyldig strekkode');
        return; // could not validate that a barcode was submitted
      }
    }
    if ( isset($_GET['article_id']) ) {
      $this->validate_search_string_article_id();
      if ( !($this->search_string_article_id)) {
        $this->template->message('Ugyldig artikkel id');
        return; // could not validate that an article_id was submitted
      }
    }

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Kategori' => 'category',
      'Pris' => 'price',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Lev. ID' => 'supplyid',
      'Sist Importert' => 'lastimported',
      'Sist Solgt' => 'lastsold',
    ];

    $query = new QueryRetailFindByArticle();
    $query->select_item_info();
    $this->database_retail = new DatabaseRetail();
    $this->database_retail->select_sinlge_row($query->get());
    // $query->print();
    $query = null;

    // all results are handled and printed on screen here
    if ($this->database_retail->result) {
      $article_id = $this->database_retail->result['article_id'];
      $brand = CharacterConvert::utf_to_norwegian($this->database_retail->result['brand']);
      $article = CharacterConvert::utf_to_norwegian($this->database_retail->result['article']);
      $category = CharacterConvert::utf_to_norwegian($this->database_retail->result['category']);
      $price = $this->database_retail->result['price'];
      $quantity = $this->database_retail->result['quantity'];
      $retail_location = $this->database_retail->result['location'];
      $supplyid = $this->database_retail->result['supplyid'];
      $lastimported = $this->database_retail->result['lastimported'];
      $lastsold = $this->database_retail->result['lastsold'];

      $this->template->div_start('100', 'block');

      $this->template->div_start('40', 'inline-block', 'left');
      $this->template->title($brand . ' - ' . '<i>' . $article . '</i>');

      $this->template->line_break();

      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('Antall: ', 'left');
      $this->template->_table_row_value($quantity . ' på lager.', 'left');
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->_table_row_value('Pris:', 'left');
      $this->template->_table_row_value($price . ' kr.', 'left');
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->_table_row_value('Kategori:', 'left');
      $this->template->_table_row_value($category, 'left');
      $this->template->table_row_end();
      $this->template->table_end();

      $this->template->line_break();

      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('Sist mottatt:', 'left');
      $this->template->_table_row_value($lastimported, 'left');
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->_table_row_value('Sist solgt:', 'left');
      $this->template->_table_row_value($lastsold, 'left');
      $this->template->table_row_end();
      $this->template->table_end();

      $this->template->line_break();
      $query = new QueryRetailFindByArticle();
      $query->select_barcodes_by_article_id($article_id);
      $this->database_retail->select_multi_row($query->get());
      // $query->print();
      $query = null;
      $this->template->title('Strekkoder');
      $title = 'Nå:';
      $i = 1;
      if ($this->database_retail->result) {
        $this->template->table_start();
        foreach ($this->database_retail->result as $row) {
          if ($i === 1) {
            $this->template->table_row_start();
            $this->template->_table_row_value($title, 'left');
            $this->template->_table_row_value($row['barcode'], 'left');
            $this->template->table_row_end();
            $title = 'Tidligere:';
          }
          else if ($i === 2) {
            $this->template->table_row_start();
            $this->template->_table_row_value('------------', 'left');
            $this->template->_table_row_value('----------------------', 'left');
            $this->template->table_row_end();
            $this->template->table_row_start();
            $this->template->_table_row_value($title, 'left');
            $this->template->_table_row_value($row['barcode'], 'left');
            $this->template->table_row_end();
            $title = '';
          }
          else {
            $this->template->table_row_start();
            $this->template->_table_row_value($title, 'left');
            $this->template->_table_row_value($row['barcode'], 'left');
            $this->template->table_row_end();
          }
          $i++;
        }
        $this->template->table_end();
      }

      // if we have a registered location, fetch extra location (if exists) from datawarehouse
      $has_location = false;
      if ( ($retail_location != null) and (strlen($retail_location) > 0) ) {
        $has_location = true;
      }

      // print out all placement registered for item
      if ($has_location) {
        $this->template->line_break();

        $this->template->title('Plassering');
        $this->template->table_start();
        $this->template->table_row_start();
        $this->template->_table_row_value('Nå:', 'left');
        $this->template->_table_row_value($retail_location, 'left');
        $this->template->table_row_end();
        $this->template->table_row_start();
        $this->template->_table_row_value('------------', 'left');
        $this->template->_table_row_value('--------', 'left');
        $this->template->table_row_end();
        $this->template->table_end();

        // add extra registered placement from datawarehouse
        $this->template->table_start();
        $this->database_datawarehouse = new DatabaseDatawarehouse();
        $query = new QueryDatawarehouseFind();
        $query->_select_placements_by_article_id();
        $stmt = $this->database_datawarehouse->cnxn->prepare($query->get());
        $query = null;
        $stmt->execute([':article_id' => $article_id]);
        $title = 'Tidligere:';
        if ($stmt->rowCount() > 0) {
          $arr_datawarehouse_locations = $stmt->fetchAll(PDO::FETCH_COLUMN, 0);
          foreach ($arr_datawarehouse_locations as $datawarehouse_location) {
            if ($datawarehouse_location != $retail_location) {
              $this->template->table_row_start();
              $this->template->_table_row_value($title, 'left');
              $this->template->_table_row_value($datawarehouse_location, 'left');
              $this->template->table_row_end();
              $title = '';
            }
          }
        }
        $this->template->table_end();
      }

      // end div for for left side info
      $this->template->div_end();

      if ($has_location) {
        // show placement map on right side
        $this->template->div_start('60', 'inline-block');
        $this->template->image_location($retail_location);
        $this->template->div_end();
      }
      // end div that contains item info and placement map
      $this->template->div_end();

      $this->template->css_by_barcode();
    }
  }

}
