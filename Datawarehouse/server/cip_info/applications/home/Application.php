<?php

/**
 *
 * TODO:
 *  add: overview over todays turnover with diagram
 *  add: read from "vaktliste.xls" or some other source and display whos on shift today
 *  add: show orders (need a working implementation of registering orders first)
 *  add fun stuff:
 *    pick our todays seller based in random choice (not based on most sales etc.)
 *    show what brands arrived today
 */

class Home {

  protected $page = 'Hjem';
  protected $note;
  protected $environment;
  protected $navigation;
  protected $title;
  protected $title_left;
  protected $title_right;
  protected $hyperlink;
  protected $database_retail;
  protected $query_retail;
  protected $database_dw;
  protected $query_dw;
  protected $min_customer_sales_id_today;

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Date.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/Navigation.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/home/QueryRetailHome.php';
    require_once '../applications/home/QueryDatawarehouseHome.php';

    $this->min_customer_sales_id_today = false;

    $this->environment = new Environment();
    $this->template = new TemplateHome();
    $this->navigation = new Navigation();
    $this->hyperlink = new HyperLink();

    $this->database_retail = new DatabaseRetail();
    $this->query_retail = new QueryRetailHome();
    $this->database_dw = new DatabaseDatawarehouse();
    $this->query_dw = new QueryDatawarehouseHome();

    $this->title_left = 'C.I.Pedersen';
    $this->title_right = Dates::get_this_weekday() . ' ' . date("d/m-Y");

    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

  public function run () {
    $this->template->title_left_and_right($this->title_left, $this->title_right);

    // fetch note from db cache table
    $this->home_page_note();

    // show "progress bar" for how busy (sales and sellers present) in shop at this time
    $this->template->second_title('Pågang i butikk');
    $this->template->shop_how_busy();

    // get simple reports
    $this->get_reports();

    $this->template->print($this->page);
  }

  private function get_reports () {
    $this->get_min_customer_sales_id_today();
    if ( !($this->min_customer_sales_id_today) ) {
      if ($this->environment->developement('show_debug')) {
        $this->template->message('Warning: could not get cache "min_customer_sales_id_today" for reports');
      }
      return;
    }
    // only if above block succeed, the below block will execute
    $this->turnover();
    if ($this->environment->competitive('show')) {
      $this->users_sales_metrics();
    }
    $this->most_expensive_item_sold_today();
    $this->last_ten_sold_items();
    $this->brands_imported_today();
  }

  private function get_min_customer_sales_id_today () {
    // we do not want to get yesterdays or older value
    $this->database_dw->mem_delete_yesterday('min_customer_sales_id_today');
    $this->min_customer_sales_id_today = $this->database_dw->mem_get('min_customer_sales_id_today')['mem_val'];
    if ( !($this->min_customer_sales_id_today) ) {
      $this->query_retail->get_min_customer_sales_id_today();
      $this->database_retail->select_single_row($this->query_retail->get());
      $this->min_customer_sales_id_today = $this->database_retail->result['min_id'];
      $this->database_dw->mem_insert('min_customer_sales_id_today', $this->min_customer_sales_id_today);
    }
  }

  private function home_page_note () {
    // on every page load, delete note if from yesterday
    $this->database_dw->mem_delete_yesterday('home_page_note');
    // insert new note if requested
    if(isset($_POST['note_input_form'])) {
      $this->database_dw->mem_insert('home_page_note', $_POST['note_input_form']);
    }
    // fetch note that resides currently in the database cache table
    $this->note = $this->database_dw->mem_get('home_page_note')['mem_val'];
    if ( empty($this->note) ) {
      $this->note = '';
    }
    // show note
    $this->template->second_title('Notat');
    $this->template->note_input_form($this->note);
    $this->template->message('Husk: alle kan legge til, endre eller fjerne notater og disse forsvinner etter 1 dag');
  }

  private function turnover () {
    $this->query_retail->turnover_today($this->min_customer_sales_id_today);
    $this->database_retail->select_single_row($this->query_retail->get());
    if ( !($this->database_retail->result) ) {
      return;
    }
    $turnover_today = $this->database_retail->result;
    $this->template->second_title('Omsetning i dag kr. ' . $turnover_today['sum_turnover'] . ' og omsetning samme dag');
    $weeks_behind = [
      1 => null,
      2 => null,
      3 => null,
      4 => null,
      52 => null,
    ];

    foreach ($weeks_behind as $i => $val) {
      $s_i = strval($i);
      $turnover = null;
      $this->database_dw->mem_delete_yesterday('turnover_week_behind_' . $s_i);
      $mem = $this->database_dw->mem_get('turnover_week_behind_' . $s_i);
      if ( !(empty($mem)) ) {
        $weeks_behind[$i] = $mem['mem_val'];
      }
      if ( $weeks_behind[$i] === null ) {
        // if null, no cache was grabbed and we need to fetch from retail
        $this->query_retail->turnover_week_behind($i);
        $this->database_retail->select_single_row($this->query_retail->get());
        if ($this->database_retail->result) {
          $turnover = $this->database_retail->result['sum_turnover'];
          $this->database_dw->mem_insert('turnover_week_behind_' . $s_i, $turnover);
          $weeks_behind[$i] = $turnover;
        }
      }
    }
    $this->template->table_start();

    $this->template->table_row_start();
    foreach ($weeks_behind as $i => $val) {
      $s = strval($i);
      $m = 'uke' . str_repeat('r', ($i != 1) * 1);
      $this->template->table_row_value('|');
      $this->template->_table_row_value("$s $m siden", 'center');
    }
    $this->template->table_row_value('|');
    $this->template->table_row_end();

    $this->template->table_row_start();
    foreach ($weeks_behind as $i => $val) {
      $this->template->table_row_value('|');
      $this->template->_table_row_value('kr. <strong>' . $val . '</strong>', 'center');
    }
    $this->template->table_row_value('|');
    $this->template->table_row_end();

    $this->template->table_end();
  }

  private function most_expensive_item_sold_today () {
    $this->query_retail->most_expensive_item_sold_today($this->min_customer_sales_id_today);
    $this->database_retail->select_single_row($this->query_retail->get());
    if ($this->database_retail->result) {
      $price = $this->database_retail->result['price'];
      $brand = CharacterConvert::utf_to_norwegian($this->database_retail->result['brand']);
      $article = CharacterConvert::utf_to_norwegian($this->database_retail->result['article']);
      $this->hyperlink->link_redirect_query('find/byarticle', 'article_id', $this->database_retail->result['article_id']);
      $_l = $brand . ' - ' . $article;
      if (strlen($brand) < 2 or $brand == null) {
        $_l = $article;
      }
      $soldqty = $this->database_retail->result['soldqty'];
      $salesperson = CharacterConvert::utf_to_norwegian($this->database_retail->result['salesperson']);
      $time = $this->database_retail->result['time'];
      $this->template->second_title('Største salg i dag til kr. ' . $price);
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_value($soldqty . ' stk ' . $_l, $this->hyperlink->url);
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->table_row_value('Solgt av ' . $salesperson . ' klokken ' . $time);
      $this->template->table_row_end();
      $this->template->table_end();
    }
  }

  private function last_ten_sold_items () {
    $this->query_retail->last_ten_sold_items($this->min_customer_sales_id_today);
    $this->database_retail->select_multi_row($this->query_retail->get());
    if ($this->database_retail->result) {
      $this->template->second_title('Siste 10 salg i dag');
      $this->template->table_full_width_start();
      $this->template->table_row_start();
      $this->template->table_row_value('<strong>Selger</strong>');
      $this->template->table_row_value('<strong>Tid</strong>');
      $this->template->table_row_value('<strong>Artikkel</strong>');
      $this->template->table_row_end();
      foreach ($this->database_retail->result as $row) {
        $article_id = $row['article_id'];
        $this->hyperlink->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $brand = CharacterConvert::utf_to_norwegian($row['brand']);
        $article = CharacterConvert::utf_to_norwegian($row['article']);
        $this->template->table_row_start();
        $this->template->table_row_value('| ' . $row['seller']);
        $this->template->table_row_value('| ' . $row['time']);
        $this->template->table_row_value('| ' . $brand . ' - ' . $article, $this->hyperlink->url);
        $this->template->table_row_end();
      }
      $this->template->table_end();
      $this->hyperlink->link_redirect('reports/sales');
      $this->template->hyperlink_button('Se alle salg', $this->hyperlink->url);
    }
  }

  private function brands_imported_today () {
    $this->query_retail->brands_imported_today();
    $this->database_retail->select_multi_row($this->query_retail->get());
    if ($this->database_retail->result) {
      $this->template->second_title('Varer fra disse leverandørene har kommet inn idag');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('<strong>Merke</strong>', 'left');
      $this->template->_table_row_value('<strong>Antall</strong>', 'left');
      $this->template->table_row_end();
      foreach ($this->database_retail->result as $row) {
        $this->template->table_row_start();
        $this->template->_table_row_value('| ' . CharacterConvert::utf_to_norwegian($row['brand']), 'left');
        $this->template->_table_row_value('| ' . $row['articles_imported'], 'left');
        $this->template->table_row_end();
      }
      $this->template->table_end();
      $this->hyperlink->link_redirect('reports/imported');
      $this->template->hyperlink_button('Se alle', $this->hyperlink->url);
    }
  }

  private function users_sales_metrics () {
    $this->query_retail->users_sales_metrics($this->min_customer_sales_id_today);
    $this->database_retail->select_multi_row($this->query_retail->get());
    if ($this->database_retail->result) {
      $this->template->second_title('Salgsfordeling i dag');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('<strong>Selger</strong>', 'left');
      $this->template->_table_row_value('<strong>Antal</strong>', 'left');
      $this->template->_table_row_value('<strong>Total</strong>', 'left');
      $this->template->table_row_end();
      foreach ($this->database_retail->result as $row) {
        $this->template->table_row_start();
        $this->template->_table_row_value('| ' . CharacterConvert::utf_to_norwegian($row['salesperson']), 'left');
        $this->template->_table_row_value('| ' . $row['article_count'], 'left');
        $this->template->_table_row_value('| ' . $row['total'] . ' kr.', 'left');
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

}
