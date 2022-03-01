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

  protected $page = 'Rapporter';
  protected $navigation;
  protected $template;
  protected $config;
  protected $visitor_url;
  protected $order;
  protected $hyper_link;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/reports/NavigationReports.php';
    require_once '../applications/reports/TemplateReports.php';
    require_once '../applications/reports/QueryReports.php';

    // default is ascending, but we flip the order of rows if ascending is already set
    $this->order = 'ascending';
    if (isset($_GET['order'])) {
      if ($_GET['order'] == 'ascending') {
        $this->order = 'descending';
      }
    }

    $config_file = '../../../../environment.ini';
    $this->config = parse_ini_file($config_file, $process_sections = true);
    $this->navigation = new NavigationReports();
    $this->template = new TemplateReports();
    $this->template->start();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);

  }
}

class Home extends Reports {
  public function run () {

    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->title('Rapporter');
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
        $left_title = 'Rapport: Utsolgte varer i dag';
        break;
      case 'thisweek':
        $left_title = 'Rapport: Utsolgte varer denne uken';
      break;
      case 'thismonth':
        $left_title = 'Rapport: Utsolgte varer '. Dates::get_this_month() . ' ' . date("Y");
      break;
    }
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");
    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'quantity',
      'Plassering' => 'location',
      'Sist Importert' => 'lastimported',
      'Sist Solgt' => 'lastsold',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->title_left($left_title);
    $this->template->title_right($right_title);

    $this->template->table_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    foreach ($table_headers as $alias => $name) {
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      // $header_val = '<a href="' . $hyperlink_header->url . '" style="width: 100%;">' . $alias . '</a>';
      // $this->template->table_row_header($header_val);
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    $this->template->table_row_end();
    $query = QuerySoldout::get($type);
    $this->cnxn = Database::get_retail_connection();
    try {
      foreach ($this->cnxn->query($query) as $row) {
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
        $left_title = 'Rapport: Importerte varer i dag';
        break;
      case 'thisweek':
        $left_title = 'Rapport: Importerte varer denne uken';
      break;
      case 'thismonth':
        $left_title = 'Rapport: Importerte varer '. Dates::get_this_month() . ' ' . date("Y");
      break;
    }
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");
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

    $this->template->title_left($left_title);
    $this->template->title_right($right_title);

    $this->template->table_start();
    $this->template->table_row_start();

    $hyperlink_header = new HyperLink();
    foreach ($table_headers as $alias => $name) {
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      // $header_val = '<a href="' . $hyperlink_header->url . '" style="width: 100%;">' . $alias . '</a>';
      // $this->template->table_row_header($header_val);
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    $this->template->table_row_end();
    $query = QueryImported::get($type);
    $this->cnxn = Database::get_retail_connection();
    try {
      foreach ($this->cnxn->query($query) as $row) {
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
        $left_title = 'Rapport: Alle salg i dag';
        break;
      case 'thisweek':
        $left_title = 'Rapport: Alle salg denne uken';
      break;
      case 'thismonth':
        $left_title = 'Rapport: Alle salg '. Dates::get_this_month() . ' ' . date("Y");
      break;
    }
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");
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

    $this->template->title_left($left_title);
    $this->template->title_right($right_title);

    // report table starts here
    $this->template->table_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    foreach ($table_headers as $alias => $name) {
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      // $header_val = '<a href="' . $hyperlink_header->url . '" style="width: 100%;">' . $alias . '</a>';
      // $this->template->table_row_header($header_val);
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    $this->template->table_row_end();
    $query = QuerySold::get($type);
    $this->cnxn = Database::get_retail_connection();
    try {
      foreach ($this->cnxn->query($query) as $row) {
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
