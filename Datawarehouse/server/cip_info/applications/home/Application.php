<?php

/**
 *
 * TODO:
 *  add: quick input box for barcode scanning
 *  add: overview over todays turnover with diagram
 *  add: read from "vaktliste.xls" or some other source and display whos on shift today
 *  add: show orders (need a working implementation of registering orders first)
 *  add fun stuff:
 *    pick our todays seller based in random choice (not based on most sales etc.)
 *    show most expensive item sold today
 *    show last 10 items sold today with user
 *    show what brands arrived today
 */

class Home {

  protected $page = 'Hjem';
  protected $environment;
  protected $navigation;
  protected $title;
  protected $title_left;
  protected $title_right;
  protected $database;
  protected $query;

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/Navigation.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/home/QueryRetailHome.php';

    $this->environment = new Environment();
    $this->template = new TemplateHome();
    $this->navigation = new Navigation();

    $this->database = new DatabaseRetail();
    $this->query = new QueryRetailHome();

    $this->title_left = 'C.I.Pedersen';
    $this->title_right = Dates::get_this_weekday() . ' ' . date("d/m-Y");

    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

  public function run () {
    $this->template->title_left_and_right($this->title_left, $this->title_right);
    // $this->user_who_sold_most_today();
    $this->most_expensive_item_sold_today();
    $this->last_ten_sold_items();
    $this->brands_imported_today();
    $this->template->print();
  }

  private function most_expensive_item_sold_today () {
    $this->query->most_expensive_item_sold_today();
    $this->database->select_sinlge_row($this->query->get());
    if ($this->database->result) {
      $res = $this->database->result;
      $this->template->second_title('Dyreste artikkel solgt idag');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_value($res['brand'] . ' - ' . $res['article']);
      $this->template->table_row_end();
      $this->template->table_row_start();
      $this->template->table_row_value('Solgt av ' . $res['salesperson'] . ' klokken ' . $res['time'] . ' til kr.' . $res['price']);
      $this->template->table_row_end();
      $this->template->table_end();
    }
  }

  private function user_who_sold_most_today () {
    $this->query->user_who_sold_most_today();
    $this->database->select_sinlge_row($this->query->get());
    if ($this->database->result) {
      $res = $this->database->result;
      $this->template->second_title('Selger med flest salg idag');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_value($res['salesperson'] . ' med ' . $res['article_count'] . ' salg');
      $this->template->table_row_end();
      $this->template->table_end();
    }
  }

  private function last_ten_sold_items () {
    $this->query->last_ten_sold_items();
    $this->database->select_multi_row($this->query->get());
    if ($this->database->result) {
      $this->template->second_title('Nylige salg');
      $hyperlink_row = new HyperLink();
      $this->template->table_full_width_start();
      $this->template->table_row_start();
      $this->template->table_row_value('<strong>Selger</strong>');
      $this->template->table_row_value('<strong>Klokke</strong>');
      $this->template->table_row_value('<strong>Artikkel</strong>');
      $this->template->table_row_end();
      foreach ($this->database->result as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $brand = CharacterConvert::utf_to_norwegian($row['brand']);
        $article = CharacterConvert::utf_to_norwegian($row['article']);
        $this->template->table_row_start();
        $this->template->table_row_value($row['seller'], $hyperlink_row->url);
        $this->template->table_row_value($row['time']);
        $this->template->table_row_value($brand . ' - ' . $article, $hyperlink_row->url);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

  private function brands_imported_today () {
    $this->query->brands_imported_today();
    $this->database->select_multi_row($this->query->get());
    if ($this->database->result) {
      $this->template->second_title('Varer fra disse merkene har kommet inn idag');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_value('<strong>Merke</strong>');
      $this->template->table_row_value('<strong>Antall</strong>');
      $this->template->table_row_end();
      foreach ($this->database->result as $row) {

        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value($row['articles_imported']);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

}
