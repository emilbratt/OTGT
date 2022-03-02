<?php

/**
 * TODO:
 * rewrite QueryReports.php from static methods to instance methods
 * add turnover reports, maybe include graphs using some graphing tool for web view
 * add: filter rows on reports
 * example request: http://host:port/reports/soldout?type=thismonth&include=none-defaults&filter=default&sort=brand&order=accendings
 *
 */

class Reports {

  protected $page = 'Rapporter'; // alias for top_navbar
  protected $title_left = 'Rapport: ';
  protected $title_right;
  protected $navigation;
  protected $template;
  protected $table_headers;
  protected $config;
  protected $visitor_url;
  protected $sort_by; // keeping track of what column is sorted by
  protected $order; // keeping track of what order should be passed when clicking header col of result table
  protected $arrow_symbol; // show arrow pointing at the way the table is ordered
  protected $hyper_link;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/Date.php';
    require_once '../applications/reports/NavigationReports.php';
    require_once '../applications/reports/TemplateReports.php';
    require_once '../applications/reports/QueryReports.php';

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

    $config_file = '../../../../environment.ini';
    $this->config = parse_ini_file($config_file, $process_sections = true);

    $this->navigation = new NavigationReports();
    $this->template = new TemplateReports();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }
}

class Home extends Reports {
  public function run () {

    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
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
    $this->title_right = 'Dato idag: ' . Dates::get_this_weekday() . ' ' . date("d/m-Y");

    $this->table_headers = [
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

    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    foreach ($this->table_headers as $alias => $name) {
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    $this->template->table_row_end();

    $query = new QueryReports();
    $query->sold_out();
    // $query->print();
    $this->cnxn = Database::get_retail_connection();
    try {
      foreach ($this->cnxn->query($query->get()) as $row) {
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['lastimported']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['lastsold']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['supplyid']));
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->config['developement']['show_errors']) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();

    $this->template->print();
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
        $this->title_left .= ' Importerte varer i dag';
        break;
      case 'thisweek':
        $this->title_left .= ' Importerte varer denne uken';
      break;
      case 'thismonth':
        $this->title_left .= ' Importerte varer ' . Dates::get_this_month() . ' ' . date("Y");
      break;
      default:
        $date = new Date();
        $date->format_from_string($type);
        $this->title_left .= ' Importerte varer ' . $date->display;
    }
    $this->title_right = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");
    $_key = 'Dato';
    if ($type == 'thisday') {
      $_key = 'Tid';
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
    $this->cnxn = Database::get_retail_connection();
    try {
      foreach ($this->cnxn->query($query->get()) as $row) {
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['import_qty']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['lastimported']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['supplyid']));
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->config['developement']['show_errors']) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();

    $this->template->print();
  }

}


class Sold extends Reports {

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
    $this->title_right = 'Dato idag: ' . Dates::get_this_weekday() . ' ' . date("d/m-Y");

    $_key = 'Dato';
    if ($type == 'thisday') {
      $_key = 'Tid';
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
    $query->sold();
    // $query->print();
    $this->cnxn = Database::get_retail_connection();
    try {
      foreach ($this->cnxn->query($query->get()) as $row) {
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['name']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['soldqty']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['salesdate']));
        $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row['price']));
        $this->template->table_row_end();
      }
    }
    catch(Exception $e)  {
      if($this->config['developement']['show_errors']) {
        echo '<pre>';
        print_r($e->getMessage());
        echo $query;
        echo '</pre>';
      }
      exit(1);
    }
    $this->template->table_end();

    $this->template->print();
  }

}
