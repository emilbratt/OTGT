<?php

class Find {

  protected $page = 'Finn Vare';
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
  protected $user_input_ok;
  protected $toggle_expired_message;
  protected $search_string_barcode;
  protected $search_string_article_id;
  const ADJUSTMENT_CODE = [
    '9' =>'salg', // NOTE: N < 0 = removed from sales header "fjernet fra bong"
    '10' => 'kreditering', // NOTE: N = cancels out N sale (code 9)
    '41' => 'varemottak',
    '1' =>'korreksjon minus',
    '2' =>'korreksjon pluss',
    '3' =>'telling',
    '4' =>'mottak fra bestilling',
    '33' => 'tilleggende telling',
    '91' => 'intern pakkeseddel el. web-pakkeseddel',
  ];

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/find/NavigationFind.php';
    require_once '../applications/find/TemplateFind.php';
    require_once '../applications/find/QueryRetailFind.php';
    require_once '../applications/find/QueryDatawarehouseFind.php';

    $this->environment = new Environment();
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

  protected function validate_search_string_barcode () {
    $check_num = is_numeric($_GET['input_field_barcode']);
    $check_len = (strlen($_GET['input_field_barcode']) < 14 or strlen($_GET['input_field_barcode']) > 7);
    $this->search_string_barcode = ($check_num == true and $check_len == true);
  }
  protected function validate_search_string_article_id () {
    $this->search_string_article_id = is_numeric($_GET['article_id']);
  }

}


class Home extends Find {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->form_barcode($action = 'find/byarticle');
    $this->template->print($this->page);
  }

}


class BySearch extends Find {

  /*
   * list a result table based on kewords for article name and
   * brand name passed by the user
   * clicking on one article from result loads the "ByArticle" class
   */

  public function run () {
    // if form is passed, handle query and show result table
    $this->template->form_search('byarticles');

    if ( isset($_GET['input_field_brand'])
    or   isset($_GET['input_field_article'])
    or   isset($_GET['input_field_supplyid']) ) {
      $this->validate_user_input();
      if ($this->user_input_ok) {
        $this->result_set();
        $this->template->css_search_result_set();
      }
    }
    $this->template->print($this->page);
  }

  private function validate_user_input () {
    // if search string is to short, the query will become to expensive
    // and potentially to many rows; we set a lower limit to characters
    $this->user_input_ok = false;

    $a = $_GET['input_field_article'];
    $b = $_GET['input_field_brand'];
    $s = $_GET['input_field_supplyid'];

    // user might have scanned an item with EAN number, check this first
    if ( is_numeric($a) ) {
      if ( strlen($a) > 10 ) {
        $hyperlink = new HyperLink();
        $hyperlink->link_redirect('find/byarticle');
        $this->template->message('Er dette en strekkode: ' . $a);
        $this->template->message('Søkestrengen inneholder kun tall og du søker på varer nå');
        $this->template->message('..hvis du ønsker å skanne en vare så trykker du knappen under');
        $this->template->hyperlink_button('Skann Vare', $hyperlink->url);
        $this->template->line_break();
        $this->template->line_break();
      }
    }

    // if the total search string across all input has 0, it most likely is a miss-click
    if (strlen($b . $s . $a) < 1) {
      return;
    }

    // if article string is less than 4 characters
    if ( strlen($a) < 4 ) {
      if ( strlen($b . $s) == 0 ) {
        $this->template->message('Bruk minst 4 tegn på å søke på artikkel hvis andre felt er tomme');
        return;
      }
    }

    // if brand string is less than 3 characters
    if ( strlen($b) < 3 ) {
      if ( strlen($a . $s) == 0 ) {
        $this->template->message('Bruk minst 3 tegn på å søke på merke hvis andre felt er tomme');
        return;
      }
    }

    // if supplyid string is less than 3 characters
    if ( strlen($s) < 3 ) {
      if ( strlen($a . $b) == 0 ) {
        $this->template->message('Bruk minst 3 tegn på å søke på Leverandør-id hvis andre felt er tomme');
        return;
      }
    }

    $this->user_input_ok = true;
  }

  private function result_set () {
    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('items', $this->toggle_expired);

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'stock_quantity',
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
    $query->select_fields();
    $query->where_brand();
    $query->where_article();
    $query->where_supplyid();
    $query->where_article_expired();
    $query->sort_by();
    // $query->print();
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
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($row['brand']));
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($row['article']), $hyperlink_row->url);
        $this->template->table_row_value($row['stock_quantity']);
        $this->template->table_row_value($row['location'], $hyperlink_row->url);
        $this->template->table_row_value($row['supplyid'] . ' // ' . $barcode);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

}


class ByShelf extends Find {

    public function run () {
      $this->template->css_search_result_set();
      if( isset($_GET['input_field_shelf']) ) {
        $this->template->form_shelf();
          $this->validate_user_input();
        if ($this->user_input_ok) {
          $this->result_set();
        }
      }
      else {
        $this->template->message('Søk på plassering');
        $this->template->form_shelf();
      }
      $this->template->print($this->page);
    }

    private function validate_user_input () {
      $this->user_input_ok = false;
      $search_string_shelf_len = strlen($_GET['input_field_shelf']);

      if ($search_string_shelf_len < 1) {
        return;
      }
      $this->user_input_ok = true;
    }

  private function result_set () {
    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('items', $this->toggle_expired);

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'stock_quantity',
      'Plassering' => 'location',
      'Lev. ID & Strekkode' => 'supplyid',
    ];

    $query = new QueryRetailFindBySearch();
    $query->select_fields();
    $query->where_shelf();
    $query->where_article_expired();
    $query->sort_by();
    $this->database_retail = new DatabaseRetail();
    $this->database_retail->select_multi_row($query->get());
    $query = null;
    if ($this->database_retail->result) {
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
      $hyperlink_row = new HyperLink();
      foreach ($this->database_retail->result as $row) {
        $article_id = $row['article_id'];
        $barcode = $row['barcode'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($row['brand']));
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($row['article']), $hyperlink_row->url);
        $this->template->table_row_value($row['stock_quantity']);
        $this->template->table_row_value($row['location'], $hyperlink_row->url);
        $this->template->table_row_value($row['supplyid'] . ' // ' . $barcode);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
    else {
      // to avoid no results if search for item, we show button to find/bysearch
      // ..maybe user thought he/she was searching for items and not location
      $hyperlink = new HyperLink();
      $hyperlink->link_redirect('find/bysearch');
      $this->template->message('Du søker på plassering nå');
      $this->template->hyperlink_button('Søk på varer her', $hyperlink->url);
    }
  }

}


class ByArticle extends Find {

  /*
   * displays data for one article
   */

  public function run () {
    $this->template->form_barcode();

    // if form is passed or get request with article id, handle request
    if ( isset($_GET['input_field_barcode']) or isset($_GET['article_id']) ) {
      $this->get_article_result();
    }

    $this->template->print($this->page);
  }

  private function get_article_result () {
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

    $query = new QueryRetailFindByArticle();
    $query->select_item_info();
    // $query->print();
    $this->database_retail = new DatabaseRetail();
    $this->database_retail->select_single_row($query->get());
    $query = null;

    // all results are handled and printed on screen here
    if ($this->database_retail->result) {
      $this->template->css_article_info();
      $article_id = $this->database_retail->result['article_id'];
      $brand = CharacterConvert::iso_8859_1_to_utf_8($this->database_retail->result['brand']);
      $article = CharacterConvert::iso_8859_1_to_utf_8($this->database_retail->result['article']);
      $category = CharacterConvert::iso_8859_1_to_utf_8($this->database_retail->result['category']);
      $price = $this->database_retail->result['price'];
      $stock_quantity = $this->database_retail->result['stock_quantity'];
      $retail_location = $this->database_retail->result['location'];
      $supplyid = $this->database_retail->result['supplyid'];
      $lastimported = $this->database_retail->result['lastimported'];
      $lastsold = $this->database_retail->result['lastsold'];
      $hyperlink = new HyperLink();
      $hyperlink->link_redirect_query('find/articlemovement', 'article_id', $article_id);
      $this->template->hyperlink_button('Varebevegelse', $hyperlink->url);

      $this->template->div_start('100', 'block');

      $this->template->div_start('40', 'inline-block', 'left');
      $this->template->title($brand . ' - ' . '<i>' . $article . '</i>');

      $this->template->line_break();

      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('Antall: ', 'left');
      $this->template->_table_row_value($stock_quantity . ' på lager.', 'left');
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->_table_row_value('Pris:', 'left');
      $this->template->_table_row_value($price . ' kr.', 'left');
      $this->template->table_row_end();
      $this->template->table_end();

      $this->template->line_break();

      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('Kategori:', 'left');
      $this->template->_table_row_value($category, 'left');
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->_table_row_value('Lev.ID:', 'left');
      $this->template->_table_row_value($supplyid, 'left');
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
      $this->template->sales_count($article_id);

      $query = new QueryRetailFindByArticle();
      $query->select_barcodes_by_article_id($article_id);
      $this->database_retail->select_multi_row($query->get());
      // $query->print();
      $query = null;

      $this->template->_title('Plassering');
      $this->template->button_fetch_api_post_update_placement($article_id);
      $has_location = false;
      if ( ($retail_location != null) and (strlen($retail_location) > 0) ) {
        // print out all placement registered for item
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

      $this->template->title('Strekkoder');
      $title = 'På pristag:';
      $i = 1;
      if ($this->database_retail->result) {
        $this->template->table_start();
        foreach ($this->database_retail->result as $row) {
          if ($i === 1) {
            $this->template->table_row_start();
            $this->template->_table_row_value($title, 'left');
            $this->template->_table_row_value($row['barcode'], 'left');
            $this->template->table_row_end();
            $title = 'Også i bruk:';
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
      // end div for for left side info
      $this->template->div_end();

      // show placement map on right side
      $this->template->div_start('60', 'inline-block');
      $this->template->image_location($retail_location);
      // end div for right side info
      $this->template->div_end();

      // end div for both sides
      $this->template->div_end();
    }
  }

}

class ArticleMovement extends Find {

  /*
   * list a result table showing all movements for article
   */

  public function run () {
    $this->template->css_article_movement_result_set();
    $this->template->form_barcode('articlemovement');
    if ( isset($_GET['input_field_barcode']) or isset($_GET['article_id']) ) {
      $this->get_article_movement_result();
    }
    $this->template->print($this->page);
  }

  private function get_article_movement_result () {
    $query = new QueryRetailFindArticleMovement();
    $this->database_retail = new DatabaseRetail();
    $query->article_info();
    $this->database_retail->select_single_row($query->get());
    if ($this->database_retail->result) {
      $article_id = $this->database_retail->result['article_id'];
      $brand = CharacterConvert::iso_8859_1_to_utf_8($this->database_retail->result['brand']);
      $article = CharacterConvert::iso_8859_1_to_utf_8($this->database_retail->result['article']);
      $quantity = $this->database_retail->result['stock_quantity'];
      $supplyid = $this->database_retail->result['supplyid'];
    } else {
      return;
    }

    $query->select_article_movement_summary();
    $this->database_retail->select_multi_row($query->get());
    // $query->print();
    if ($this->database_retail->result) {
      // link to show ordinary item info
      $hyperlink = new HyperLink();
      $hyperlink->link_redirect_query('find/byarticle', 'article_id', $article_id);
      $this->template->hyperlink_button('Vareinfo', $hyperlink->url);
      $this->template->title($brand . ' - ' . '<i>' . $article . '</i>');

      $this->template->line_break();

      // prepare result-set to fit the layout we want
      $arr_new = array();
      $year = $this->database_retail->result[0]['yyyy'];
      $arr_years = [$year];
      foreach ($this->database_retail->result as $row) {
        $arr_new[$row['movement']][$row['yyyy']] = intval($row['qty']);
        if ( intval($row['yyyy'] < $year) ) {
          $year = intval($row['yyyy']);
          array_push($arr_years, $year);
        }
        $arr_cur[$row['movement']] = $row['qty'];
      }
      // if removed from salesheader (fjernet fra bong), we subtract that value and only yse sales-count
      if ( isset($arr_new[self::ADJUSTMENT_CODE[10]]) ) {
        foreach ($arr_new[self::ADJUSTMENT_CODE[10]] as $key => $qty) {
          if ( isset($arr_new[self::ADJUSTMENT_CODE[9]][$key]) ) {
            $arr_new [self::ADJUSTMENT_CODE[9]][$key] -=$qty;
          }
        }
      }
      unset($arr_new[self::ADJUSTMENT_CODE[10]]);

      // I only want to include records from these adjustmend codes
      $included_codes = [9, 41, 2, 1, 3];

      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_value('År');
      // create a total summary with an array holding the total
      $arr_rollup = array();
        foreach ($included_codes as $code) {
          $this->template->table_row_value (ucfirst(self::ADJUSTMENT_CODE[$code]));
          $arr_rollup[$code] = 0;
        }
      $this->template->table_row_end();
      foreach ($arr_years as $year) {
        $this->template->table_row_start();
        $this->template->table_row_value($year);
        foreach ($included_codes as $code) {
          $val = 0;
          if ( isset($arr_new[self::ADJUSTMENT_CODE[$code]][$year]) ) {
            $val = intval($arr_new[self::ADJUSTMENT_CODE[$code]][$year]);
          }
          $arr_rollup[$code] += $val;
          $this->template->table_row_value(strval($val));
        }
        $this->template->table_row_end();
      }
      // show total sum for each category using rollup array
      $this->template->table_row_start();
      $this->template->table_row_value('Total');
      foreach ($arr_rollup as $total) {
        $this->template->table_row_value(strval($total));
      }
      $this->template->table_row_end();
      $this->template->table_end();
    }
  }

}
