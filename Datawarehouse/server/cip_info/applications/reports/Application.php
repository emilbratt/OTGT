<?php

/**
 * notes:
 * for turnover reports, maybe include graphs using some graphing tool for web view
 *
 * example request: http://host:port/reports/soldout/&type=thismonth&include=none-defaults&filter=default&sort=brand&order=accendings
 *
 */

class Reports {

  protected $visitor_url;
  protected $order;
  protected $hyper_link;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/reports/ReportTemplate.php';
    require_once '../applications/reports/QueryReports.php';

    // default is ascending, but we flip the order of rows if ascending is already set
    $this->order = 'ascending';
    if (isset($_GET['order'])) {
      if ($_GET['order'] == 'ascending') {
        $this->order = 'descending';
      }
    }
  }

  public function run () {
    echo 'this is reports Rerports()';
  }

  protected function add_query_parameter ($old_url, $key, $val) {
    // first, remove or replace with empty string if key exist
    // regex: starts with either ? or & followed by $key followed by = and any value until & or end of string
    $filtered_url = preg_replace('/(\?|&)'.$key.'=[^&]*/', '', $old_url);
    // then add key=val to the end of the url
    $new_url = $filtered_url . '&' . "$key=$val";
    return $new_url;
  }
}


class Home extends Reports {

  public function run () {
    // links to the reports listed as classes below
    $template = new ReportTemplate();
    $template->start();
    $template->title_left('this is reports -> home');
    $template->title_right('not done yet');
    $template->end();
    $template->print();
    die;

    $reports = [
      'Utsolgt idag' => '/reports/soldout&type=thisday',
      'Utsolgt denne uken' => '/reports/soldout&type=thisweek',
    ];
    foreach ($reports as $name => $page) {
      echo '<a href="http://'.$_SERVER['HTTP_HOST'].$page.'">'.$name.'</a><br>';
    }
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
      ['Merke', 'brand'],
      ['Navn', 'article'],
      ['Lager', 'quantity'],
      ['Plassering', 'location'],
      ['Sist Importert', 'lastimported'],
      ['Sist Solgt', 'lastsold'],
      ['Lev. ID', 'supplyid'],
    ];

    // html starts here
    $template = new ReportTemplate();
    $template->start();
    $template->title_left($left_title);
    $template->title_right($right_title);

    // report table starts here
    $template->table_start();
    $template->table_row_start();
    $this->hyper_link = new HyperLink();
    foreach ($table_headers as $header) {
      $this->hyper_link->add_query('sort', $header[1]);
      $this->hyper_link->add_query('order', $this->order);
      $header_val = '<a href="' . $this->hyper_link->url . '">' . $header[0] .'</a>';
      $template->table_row_header($header_val);
    }
    $template->table_row_end();
    $query = QuerySoldout::get($type);
    $this->cnxn = Database::get_connection();
    try {
      foreach ($this->cnxn->query($query) as $row) {
        $template->table_row_start();
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['lastimported']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['lastsold']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['supplyid']));
        $template->table_row_end();
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
    $template->table_end();

    // html ends here
    $template->end();

    // prints out the whole template that is generated
    $template->print();
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

    $table_headers = [
      ['Merke', 'brand'],
      ['Navn', 'article'],
      ['Importert', 'import_qty'],
      ['Lager', 'quantity'],
      ['Plassering', 'location'],
      ['Importert', 'lastimported'],
      ['Lev. ID', 'supplyid'],
    ];

    // html starts here
    $template = new ReportTemplate();
    $template->start();
    $template->title_left($left_title);
    $template->title_right($right_title);

    // report table starts here
    $template->table_start();
    $template->table_row_start();

    $this->hyper_link = new HyperLink();
    foreach ($table_headers as $header) {
      $this->hyper_link->add_query('sort', $header[1]);
      $this->hyper_link->add_query('order', $this->order);
      $header_val = '<a href="' . $this->hyper_link->url . '">' . $header[0] .'</a>';
      $template->table_row_header($header_val);
    }
    $template->table_row_end();
    $query = QueryImported::get($type);
    $this->cnxn = Database::get_connection();
    try {
      foreach ($this->cnxn->query($query) as $row) {
        $template->table_row_start();
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['import_qty']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['lastimported']));
        $template->table_row_value(CharacterConvert::utf_to_norwegian($row['supplyid']));
        $template->table_row_end();
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
    $template->table_end();

    // html ends here
    $template->end();

    // prints out the whole template that is generated
    $template->print();
  }
}
