<?php

/**
 *
 *  TODO:
 *    add turnover reports, maybe include graphs using some graphing tool for web view
 *
 */

class Reports {

  protected $page = 'Rapporter'; // alias for top_navbar
  protected $environment;
  protected $title_left = 'Rapport: ';
  protected $title_right;
  protected $database;
  protected $navigation;
  protected $template;
  protected $table_headers;
  protected $visitor_url;
  protected $sort_by; // keeping track of what column is sorted by
  protected $order; // keeping track of what order should be passed when clicking header col of result table
  protected $arrow_symbol; // show arrow pointing at the way the table is ordered
  protected $hyper_link;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Environment.php';
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/Date.php';
    require_once '../applications/reports/NavigationReports.php';
    require_once '../applications/reports/TemplateReports.php';
    require_once '../applications/reports/QueryReports.php';

    $this->title_right = 'Dato idag: ' . Dates::get_this_weekday() . ' ' . date("d/m-Y");

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

    $this->environment = new Environment();
    $this->navigation = new NavigationReports();
    $this->database = new DatabaseRetail();
    $this->template = new TemplateReports();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }
}

class Home extends Reports {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print($this->page);
  }

}


class Soldout extends Reports {

  public function run () {
    $type = 'thisday';
    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'thisday':
        $this->title_left .= ' Utsolgte varer i dag';
        break;
      case 'thisweek':
        $this->title_left .= ' Utsolgte varer denne uken';
      break;
      case 'thismonth':
        $this->title_left .= ' Utsolgte varer '. Dates::get_this_month() . ' ' . date("Y");
      break;
      default:
        $date = new Date();
        $date->format_from_string($type);
        $this->title_left .= ' Utsolgte varer ' . $date->display;
    }

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Sist Importert' => 'lastimported',
      'Sist Solgt' => 'lastsold',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->reports_form_input_date();

    $hyperlink_time_span = new HyperLink();
    $hyperlink_time_span->add_query('type', 'thisday');
    $this->template->hyperlink_button('Idag', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('type', 'thisweek');
    $this->template->hyperlink_button('Denne Uka', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('type', 'thismonth');
    $this->template->hyperlink_button('Denn Måneden', $hyperlink_time_span->url);

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
    $hyperlink_header = null;
    $query = new QueryReports();
    $query->sold_out();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']), $hyperlink_row->url);
        $this->template->table_row_value($row['quantity']);
        $this->template->table_row_value($row['location'], $hyperlink_row->url);
        $this->template->table_row_value($row['lastimported']);
        $this->template->table_row_value($row['lastsold']);
        $this->template->table_row_value($row['supplyid']);
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();

    $this->template->print($this->page);
  }

}


class Imported extends Reports {

  public function run () {
    $type = 'thisday';
    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'thisday':
        $this->title_left .= ' Mottatte varer i dag';
        break;
      case 'thisweek':
        $this->title_left .= ' Mottatte varer denne uken';
      break;
      case 'thismonth':
        $this->title_left .= ' Mottatte varer ' . Dates::get_this_month() . ' ' . date("Y");
      break;
      default:
        $date = new Date();
        $date->format_from_string($type);
        $this->title_left .= ' Mottatte varer ' . $date->display;
    }
    $_key = 'Tid';
    if ($type == 'thisweek' or $type == 'thismonth') {
      $_key = 'Dato';
    }
    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Importert' => 'importquantity',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      $_key => 'lastimported',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->reports_form_input_date();

    $hyperlink_time_span = new HyperLink();
    $hyperlink_time_span->add_query('type', 'thisday');
    $this->template->hyperlink_button('Idag', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('type', 'thisweek');
    $this->template->hyperlink_button('Denne Uka', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('type', 'thismonth');
    $this->template->hyperlink_button('Denn Måneden', $hyperlink_time_span->url);

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
    $query = new QueryReports();
    $query->imported();
    // $query->print();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']), $hyperlink_row->url);
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['import_qty']));
        $this->template->table_row_value($row['quantity']);
        $this->template->table_row_value($row['location'], $hyperlink_row->url);
        $this->template->table_row_value($row['lastimported']);
        $this->template->table_row_value($row['supplyid']);
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();
    $hyperlink_row = null;
    $this->template->print($this->page);
  }

}


class SalesHistory extends Reports {

  public function run () {
    $type = 'thisday';
    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'thisday':
        $this->title_left .= ' Alle salg i dag';
        break;
      case 'thisweek':
        $this->title_left .= ' Alle salg denne uken';
      break;
      case 'thismonth':
        $this->title_left .= ' Alle salg '. Dates::get_this_month() . ' ' . date("Y");
      break;
      default:
        $date = new Date();
        $date->format_from_string($type);
        $this->title_left .= ' Alle salg ' . $date->display;
    }

    $_key = 'Tid';
    if ($type == 'thisweek' or $type == 'thismonth') {
      $_key = 'Dato';
    }
    $table_headers = [
      'Selger' => 'name',
      'Merke' => 'brand',
      'Navn' => 'article',
      'Antall' => 'soldqty',
      $_key => 'salesdate',
      'Pris' => 'price',
    ];

    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->reports_form_input_date();

    $hyperlink_time_span = new HyperLink();
    $hyperlink_time_span->add_query('type', 'thisday');
    $this->template->hyperlink_button('Idag', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('type', 'thisweek');
    $this->template->hyperlink_button('Denne Uka', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('type', 'thismonth');
    $this->template->hyperlink_button('Denn Måneden', $hyperlink_time_span->url);

    $this->template->script_filter_row_button('2');
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
    $query = new QueryReports();
    $query->sales_history();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['name']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']), $hyperlink_row->url);
        $this->template->table_row_value($row['soldqty']);
        $this->template->table_row_value($row['salesdate']);
        $this->template->table_row_value(round($row['price'], 2));
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();
    $hyperlink_row = null;
    $this->template->print($this->page);
  }

}


class NotSoldLately extends Reports {

  public function run () {
    $this->title_left = 'Rapport: Varer på lager som ikke er solgt på lenge';
    $this->template->title_left_and_right($this->title_left, $this->title_right);
    $this->template->reports_form_brand_year_num_stock_limit();

    if ( isset($_GET['input_field_brand'])
    and  isset($_GET['input_field_location'])
    and  isset($_GET['input_field_date_part_type'])
    and  isset($_GET['input_field_date_part_num'])
    and  isset($_GET['input_field_stock_num'])
    and  isset($_GET['input_field_stock_operator']) ) {
        $this->show_report();
    }
    $this->template->print($this->page);
  }

  private function show_report () {
    // for message string, we gather some values
    $b = $_GET['input_field_brand'];
    $l = $_GET['input_field_location'];
    $s_n = $_GET['input_field_stock_num'];
    $d_p_y = $_GET['input_field_date_part_type'];
    $arr_convert_sql_to_nor = [
      'YEAR' => 'År',
      'MONTH' => 'Måneder',
      'WEEK' => 'Uker',
      'DAY' => 'Dager',
    ];
    $d_p = $_GET['input_field_date_part_num'];
    $s_o = 'mere enn';
    if ( $_GET['input_field_stock_operator'] == '<' ) {
      $s_o = 'mindre enn';
    }
    $l = strtoupper($l);
    $this->template->message("Alle varer $b på lager $l hvor lager antall er $s_o  $s_n og ikke solgt siste $d_p $arr_convert_sql_to_nor[$d_p_y]");

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Sist Solgt' => 'lastsold',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Sist Importert' => 'lastimported',
      'Lev. ID' => 'supplyid',
    ];

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
    $query = new QueryReports();
    $query->in_stock_not_sold_lately();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']), $hyperlink_row->url);
        $this->template->table_row_value($row['lastsold']);
        $this->template->table_row_value($row['quantity']);
        $this->template->table_row_value($row['location'], $hyperlink_row->url);
        $this->template->table_row_value($row['lastimported']);
        $this->template->table_row_value($row['supplyid']);
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->environment->developement('show_errors')) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();
  }

}
