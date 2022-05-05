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
    $this->turnover();
    if ($this->environment->competitive('show')) {
      $this->users_sales_count_today();
    }
    $this->most_expensive_item_sold_today();
    $this->last_ten_sold_items();
    $this->brands_imported_today();
    $this->template->print($this->page);
  }

  private function turnover () {
    $this->query_retail->turnover_today();
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
    $date_obj = new Date();
    $date_today = $date_obj->sql_compatible_date();
    foreach ($weeks_behind as $i => $val) {
      $s_i = strval($i);
      $turnover = null;
      $mem = $this->database_dw->mem_get('turnover_week_behind_' . $s_i);
      if ( !(empty($mem)) ) {
        $cache_date = $date_obj->date_from_time_stamp($mem['mem_time']);
        if ( $cache_date == $date_today ) {
          $weeks_behind[$i] = $mem['mem_val'];
        }
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
      $this->template->table_row_value('|');
    }
    $this->template->table_row_end();
    $this->template->table_row_start();
    foreach ($weeks_behind as $i => $val) {
      $this->template->table_row_value('|');
      $this->template->_table_row_value('kr. <strong>' . $val . '</strong>', 'center');
      $this->template->table_row_value('|');
    }
    $this->template->table_row_end();
    $this->template->table_end();
  }

  private function most_expensive_item_sold_today () {
    $this->query_retail->most_expensive_item_sold_today();
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
      $salesperson = CharacterConvert::utf_to_norwegian($this->database_retail->result['salesperson']);
      $time = $this->database_retail->result['time'];
      $this->template->second_title('Dyreste artikkel solgt i dag til kr. ' . $price);
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_value($_l, $this->hyperlink->url);
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->table_row_value('Solgt av ' . $salesperson . ' klokken ' . $time);
      $this->template->table_row_end();
      $this->template->table_end();
    }
  }

  private function last_ten_sold_items () {
    $this->query_retail->last_ten_sold_items();
    $this->database_retail->select_multi_row($this->query_retail->get());
    if ($this->database_retail->result) {
      $this->template->second_title('Nylige salg');
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
      $this->template->hyperlink_button('Se alle', $this->hyperlink->url);
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

  private function users_sales_count_today () {
    $this->query_retail->users_sales_count_today();
    $this->database_retail->select_multi_row($this->query_retail->get());
    if ($this->database_retail->result) {
      $this->template->second_title('Flest salg i dag');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->_table_row_value('<strong>Selger</strong>', 'left');
      $this->template->_table_row_value('<strong>Salg</strong>', 'left');
      $this->template->table_row_end();
      foreach ($this->database_retail->result as $row) {
        $this->template->table_row_start();
        $this->template->_table_row_value('| ' . CharacterConvert::utf_to_norwegian($row['salesperson']), 'left');
        $this->template->_table_row_value('| ' . $row['article_count'], 'left');
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

}
