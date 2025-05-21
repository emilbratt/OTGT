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
  protected $data_send = array();
  protected $spreadsheet_data = array();
  protected $hyperlink_spreadsheet;
  protected $database;
  protected $navigation;
  protected $template;
  protected $table_headers;
  protected $visitor_url;
  protected $sort_by; // keeping track of what column is sorted by
  protected $order; // keeping track of what order should be passed when clicking header col of result table
  protected $arrow_symbol; // show arrow pointing at the way the table is ordered
  protected $hyper_link;
  protected $date_type;
  protected $article_status; // all items, expired items, non expired items
  protected $brand; // mainly used in reports/brand/brand_id
  protected $brand_id; // mainly used in reports/brand/brand_id
  const MONTH_CONVERT = [
    1 => 'Januar',
    2 => 'Februar',
    3 => 'Mars',
    4 => 'April',
    5 => 'Mai',
    6 => 'Juni',
    7 => 'Juli',
    8 => 'August',
    9 => 'September',
    10 => 'Oktober',
    11 => 'November',
    12 => 'Desember',
  ];
  const DAYOFWEEK_CONVERT = [
    1 => 'Mandag',
    2 => 'Tirsdag',
    3 => 'Onsdag',
    4 => 'Torsdag',
    5 => 'Fredag',
    6 => 'Lørdag',
    7 => 'Søndag',
  ];

  function __construct () {
    // session is used to store previously fetched data to generate spreadsheets
    session_start();

    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/Date.php';
    require_once '../applications/reports/NavigationReports.php';
    require_once '../applications/reports/TemplateReports.php';
    require_once '../applications/reports/QueryReports.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationReports();
    $this->database = new DatabaseRetail();
    $this->template = new TemplateReports();

    // takes url used to visit the specific page and add spreadsheet as query parameter
    $this->hyperlink_spreadsheet = new HyperLink();
    $this->hyperlink_spreadsheet->add_query('spreadsheet', 'true');

    $this->title_right = 'Dato idag: ' . Dates::get_this_weekday() . ' ' . date("d/m-Y");

    // default is none-expired (show only active articles), can be flipped with button
    $this->article_status = 'active';
    $this->article_status_message = 'Vis Kun Aktive';
    if(isset($_GET['article_status'])) {
      if($_GET['article_status'] == 'expired') {
        $this->article_status = 'all';
        $this->article_status_message = 'Vis Aktive & Utgåtte';
      }
      else if($_GET['article_status'] == 'active') {
        $this->article_status = 'expired';
        $this->article_status_message = 'Vis Kun Utgåtte';
      }
    }

    // mainly used to show date info regarding query results
    $this->date_type = 'thisday';
    if(isset($_GET['date_type'])) {
      $this->date_type = $_GET['date_type'];
    }

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

    // if clicked on button for downloading spreadsheet, new window will open in browser
    if ( isset($_GET['spreadsheet']) ) {
      if ( isset($_SESSION['spreadsheet']) ) {
        $this->send_to_api_and_generate_spreadsheet();
      }
      else {
        if ( $this->environment->developement('show_debug') ) {
          echo ("no value found in \$_SESSION['spreadsheet']");
        }
        exit(1);
      }
    }
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
    if (isset($_SESSION['message'])) {
      $this->template->message($_SESSION['message']);
      unset($_SESSION['message']);
    }
  }

  private function send_to_api_and_generate_spreadsheet () {
    $this->data_send = [
      'rows' => $_SESSION['spreadsheet'],
      'caller' => $this->environment->datawarehouse('cip_info_host'),
      'filename' => explode('/', $_SERVER['REDIRECT_URL'])[2],
      'has_header' => true,
    ];
    $host = $this->environment->datawarehouse('spreadsheet_generator_host');
    $port = $this->environment->datawarehouse('spreadsheet_generator_port');
    $url_api = 'http://'.$host.':'.$port.'/spreadsheet';
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url_api);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($this->data_send));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    // var_dump($body); die;
    if (curl_errno($curl)) {
      if ( $this->environment->developement('show_debug') ) {
        $this->template->message('Error on curl request: ' . curl_error($curl));
        $this->template->print($this->page);
        exit(1);
      }
    }
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close ($curl);
    if ($http_status_code == 201) {
      $filename = explode('/', $_SERVER['REDIRECT_URL'])[2];
      header('Content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
      header('Content-Transfer-Encoding: binary');
      header('Cache-Control: must-revalidate');
      header('Content-Disposition: attachment; filename=' . $filename . '.xlsx');
      echo $body;
      exit(0);
    }
    else if ($http_status_code == 422) {
      $m = 'Varsel: For mange rader til å skrive ut regneark<br>';
      $m .= '..reduser antall rader ved å legge til kriterier i rapporten';
      $_SESSION['message'] = $m;
    }
  }

  protected function get_left_title_date ($pre_string = '') {
    $this->title_left .= $pre_string;
    switch ($this->date_type) {
      case 'thisday':
        $this->title_left .= ' i dag';
        break;
      case 'thisweek':
        $this->title_left .= ' denne uken';
        break;
      case 'thismonth':
        $this->title_left .= ' ' . Dates::get_this_month();
        break;
      case 'calendar':
        $date = new Date();
        $date->format_from_string($_GET['calendar_from_date']);
        $date_from = $date->display;
        $date->format_from_string($_GET['calendar_to_date']);
        $date_to = $date->display;
        $this->title_left .= ' mellom ' . $date_from . ' og ' . $date_to;
        break;
    }
  }

  function __destruct() {
    $_SESSION['spreadsheet'] = $this->spreadsheet_data;
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
    $this->page = 'Utsolgt';
    $this->get_left_title_date('Utsolgte varer');

    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Lager' => 'stock_quantity',
      'Plassering' => 'location',
      'Sist Importert' => 'lastimported',
      'Sist Solgt' => 'lastsold',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->reports_form_input_date();

    $hyperlink_time_span = new HyperLink();
    $hyperlink_time_span->add_query('date_type', 'thisday');
    $this->template->hyperlink_button('I dag', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('date_type', 'thisweek');
    $this->template->hyperlink_button('Denne Uka', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('date_type', 'thismonth');
    $this->template->hyperlink_button('Denn Måneden', $hyperlink_time_span->url);

    $this->template->script_filter_row_button('1', 'Filtrer etter artikkel', $auto_focus = true);

    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('article_status', $this->article_status);
    $this->template->hyperlink_button($this->article_status_message, $hyperlink_toggle->url);

    $this->template->hyperlink_button_target_top('Last ned regneark', $this->hyperlink_spreadsheet->url);

    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    $spreadsheet_row = array();
    foreach ($table_headers as $alias => $name) {
      array_push($spreadsheet_row, $alias);
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    array_push($this->spreadsheet_data, $spreadsheet_row);
    $this->template->table_row_end();
    $hyperlink_header = null;
    $query = new QueryReports();
    $query->sold_out();
    // $query->print();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $brand = CharacterConvert::iso_8859_1_to_utf_8($row['brand']);
        $article = CharacterConvert::iso_8859_1_to_utf_8($row['article']);
        $quantity = $row['stock_quantity'];
        $location = $row['location'];
        $last_imported = $row['lastimported'];
        $lastsold = $row['lastsold'];
        $supply_id = $row['supplyid'];
        $this->template->table_row_value($brand);
        $this->template->table_row_value($article, $hyperlink_row->url);
        $this->template->table_row_value($quantity);
        $this->template->table_row_value($location, $hyperlink_row->url);
        $this->template->table_row_value($last_imported);
        $this->template->table_row_value($lastsold);
        $this->template->table_row_value($supply_id);
        $this->template->table_row_end();
        array_push($this->spreadsheet_data, [$brand, $article, intval($quantity), $location, $last_imported, $lastsold, $supply_id]);
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
    $this->page = 'Varemottak';
    $this->get_left_title_date('Mottatte varer');
    $_key = 'Dato';
    if ($this->date_type == 'thisday') {
      $_key = 'Tid';
    }
    $table_headers = [
      'Merke' => 'brand',
      'Navn' => 'article',
      'Importert' => 'importquantity',
      'Lager' => 'stock_quantity',
      'Plassering' => 'location',
      $_key => 'lastimported',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->reports_form_input_date();

    $hyperlink_time_span = new HyperLink();
    $hyperlink_time_span->add_query('date_type', 'thisday');
    $this->template->hyperlink_button('I dag', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('date_type', 'thisweek');
    $this->template->hyperlink_button('Denne Uka', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('date_type', 'thismonth');
    $this->template->hyperlink_button('Denn Måneden', $hyperlink_time_span->url);

    $this->template->script_filter_row_button(1, 'Filtrer etter artikkel', $auto_focus = true);

    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('article_status', $this->article_status);
    $this->template->hyperlink_button($this->article_status_message, $hyperlink_toggle->url);

    $this->template->hyperlink_button_target_top('Last ned regneark', $this->hyperlink_spreadsheet->url);

    $this->template->table_full_width_start();
    $this->template->table_row_start();

    $hyperlink_header = new HyperLink();
    $spreadsheet_row = array();
    foreach ($table_headers as $alias => $name) {
      array_push($spreadsheet_row, $alias);
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    array_push($this->spreadsheet_data, $spreadsheet_row);
    $this->template->table_row_end();
    $query = new QueryReports();
    $query->imported();
    // $query->print();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);

        $brand = CharacterConvert::iso_8859_1_to_utf_8($row['brand']);
        $article = CharacterConvert::iso_8859_1_to_utf_8($row['article']);
        $import_qty = $row['import_qty'];
        $stock_quantity = $row['stock_quantity'];
        $location = $row['location'];
        $last_imported = $row['lastimported'];
        $supply_id = $row['supplyid'];
        $this->template->table_row_start();
        $this->template->table_row_value($brand);
        $this->template->table_row_value($article, $hyperlink_row->url);
        $this->template->table_row_value($import_qty);
        $this->template->table_row_value($stock_quantity);
        $this->template->table_row_value($location, $hyperlink_row->url);
        $this->template->table_row_value($last_imported);
        $this->template->table_row_value($supply_id);
        $this->template->table_row_end();
        array_push($this->spreadsheet_data, [$brand, $article, intval($import_qty), intval($stock_quantity), $location, $last_imported, $supply_id]);
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


class SalesHistory extends Reports {

  public function run () {
    $this->page = 'Alle Salg';
    $this->get_left_title_date('Alle salg');
    $_key = 'Dato';
    if ($this->date_type == 'thisday') {
      $_key = 'Tid';
    }
    $table_headers = [
      'Selger' => 'seller_name',
      'Merke' => 'brand',
      'Navn' => 'article',
      'Antall' => 'soldqty',
      'Plassering' => 'location',
      $_key => 'salesdate',
      'Pris' => 'sold_price',
    ];

    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->reports_form_input_date();

    $hyperlink_time_span = new HyperLink();
    $hyperlink_time_span->add_query('date_type', 'thisday');
    $this->template->hyperlink_button('I dag', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('date_type', 'thisweek');
    $this->template->hyperlink_button('Denne Uka', $hyperlink_time_span->url);
    $hyperlink_time_span->add_query('date_type', 'thismonth');
    $this->template->hyperlink_button('Denn Måneden', $hyperlink_time_span->url);

    $this->template->script_filter_row_button('2', 'Filtrer etter artikkel', $auto_focus = true);

    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('article_status', $this->article_status);
    $this->template->hyperlink_button($this->article_status_message, $hyperlink_toggle->url);

    $this->template->hyperlink_button_target_top('Last ned regneark', $this->hyperlink_spreadsheet->url);

    $this->template->table_full_width_start();

    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    $spreadsheet_row = array();
    foreach ($table_headers as $alias => $name) {
      array_push($spreadsheet_row, $alias);
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    array_push($this->spreadsheet_data, $spreadsheet_row);
    $this->template->table_row_end();
    $query = new QueryReports();
    $query->sales_history();
    $hyperlink_row = new HyperLink();
    // $query->print();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $seller_name = CharacterConvert::iso_8859_1_to_utf_8($row['seller_name']);
        $brand = CharacterConvert::iso_8859_1_to_utf_8($row['brand']);
        $article = CharacterConvert::iso_8859_1_to_utf_8($row['article']);
        $soldqty = $row['soldqty'];
        $location = $row['location'];
        $salesdate = $row['salesdate'];
        $sold_price = round($row['sold_price'], 2);
        $this->template->table_row_start();
        $this->template->table_row_value($seller_name);
        $this->template->table_row_value($brand);
        $this->template->table_row_value($article, $hyperlink_row->url);
        $this->template->table_row_value($soldqty);
        $this->template->table_row_value($location, $hyperlink_row->url);
        $this->template->table_row_value($salesdate);
        $this->template->table_row_value($sold_price);
        $this->template->table_row_end();
        array_push($this->spreadsheet_data, [$seller_name, $brand, $article, intval($soldqty), $location, $salesdate, floatval($sold_price)]);
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


class NotSoldLately extends Reports {

  public function run () {
    $this->page = 'Ikke solgt på lenge';
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
      'Lager' => 'stock_quantity',
      'Plassering' => 'location',
      'Sist Importert' => 'lastimported',
      'Lev. ID' => 'supplyid',
    ];

    $this->template->script_filter_row_button('1', 'Filtrer etter artikkel');

    $this->template->hyperlink_button_target_top('Last ned regneark', $this->hyperlink_spreadsheet->url);

    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    $spreadsheet_row = array();
    foreach ($table_headers as $alias => $name) {
      array_push($spreadsheet_row, $alias);
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    array_push($this->spreadsheet_data, $spreadsheet_row);
    $this->template->table_row_end();
    $query = new QueryReports();
    $query->in_stock_not_sold_lately();
    // $query->print();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $brand = CharacterConvert::iso_8859_1_to_utf_8($row['brand']);
        $article = CharacterConvert::iso_8859_1_to_utf_8($row['article']);
        $lastsold = $row['lastsold'];
        $stock_quantity = $row['stock_quantity'];
        $location = $row['location'];
        $lastimported = $row['lastimported'];
        $supplyid = $row['supplyid'];
        $this->template->table_row_start();
        $this->template->table_row_value($brand);
        $this->template->table_row_value($article, $hyperlink_row->url);
        $this->template->table_row_value($lastsold);
        $this->template->table_row_value($stock_quantity);
        $this->template->table_row_value($location, $hyperlink_row->url);
        $this->template->table_row_value($lastimported);
        $this->template->table_row_value($supplyid);
        $this->template->table_row_end();
        array_push($this->spreadsheet_data, [$brand, $article, $lastsold, intval($stock_quantity), $location, $lastimported, $supplyid]);
        sleep(0.025);
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


class SalesPerHour extends Reports {

  public function run () {
    $this->page = 'Salg pr. time';
    $this->title_left = 'Rapport: Timessalg';
    $this->template->title_left_and_right($this->title_left, $this->title_right);
    $this->template->message('Felt utenom årstall er valgfritt');
    $this->template->report_form_sales_per_hour();
    if ( isset($_GET['input_field_YYYY'])
    and  isset($_GET['input_field_MM'])
    and  isset($_GET['input_field_DOM'])
    and  isset($_GET['input_field_DOW']) ) {
      $this->show_report();
    }
    $this->template->print($this->page);
  }

  private function show_report () {
    // for message string, we gather some values
    $this->add_message();

    $this->template->hyperlink_button_target_top('Last ned regneark', $this->hyperlink_spreadsheet->url);

    $table_headers = [
      'Klokketime' => 'at_hour',
      'Antall Salg' => 'total_sales',
      'Bruttosalg KR.' => 'total_net_sum',
      'Totalsalg KR.' => 'total_sum',
    ];
    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    $spreadsheet_row = array();
    foreach ($table_headers as $alias => $name) {
      array_push($spreadsheet_row, $alias);
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    array_push($this->spreadsheet_data, $spreadsheet_row);
    $this->template->table_row_end();
    $query = new QueryReports();
    $query->sales_per_hour();
    // $query->print();
    $hyperlink_row = new HyperLink();
    try {
      foreach ($this->database->cnxn->query($query->get()) as $row) {
        $at_hour = $row['at_hour'];
        $total_sales = $row['total_sales'];
        $total_net_sum = $row['total_net_sum'];
        $total_sum = $row['total_sum'];
        $this->template->table_row_start();
        $this->template->table_row_value($at_hour);
        $this->template->table_row_value($total_sales);
        $this->template->table_row_value(number_format($total_net_sum, 0, '', '.') . ',-');
        $this->template->table_row_value(number_format($total_sum, 0, '', '.') . ',-');
        $this->template->table_row_end();
        array_push($this->spreadsheet_data, [intval($at_hour), intval($total_sales), intval($total_net_sum), intval($total_sum)]);
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

  private function add_message () {
    $message = 'År: ' . $_GET['input_field_YYYY'];

    $m = 'Alle';
    if ( !(empty($_GET['input_field_MM'])) ) {
      $m = self::MONTH_CONVERT[$_GET['input_field_MM']];
    }
    $message .= '<br>Måned: ' .  $m;

    $m = 'Alle';
    if ( !(empty($_GET['input_field_DOM'])) ) {
      $m = $_GET['input_field_DOM'];
    }
    $message .= '<br>Dato: ' .  $m;

    $m = 'Alle';
    if ( !(empty($_GET['input_field_DOW'])) ) {
      $m = self::DAYOFWEEK_CONVERT[$_GET['input_field_DOW']];
    }
    $message .= '<br>Ukedag: ' . $m;

    $m = 'Alle';
    if ( !(empty($_GET['input_field_HOD'])) ) {
      $m = $_GET['input_field_HOD'];
    }
    $message .= '<br>Klokketime: ' . $m;

    $this->template->message($message);
  }

}


class Brand extends Reports {

  private $report_type;

  // uncommenting will disable buttons
  const ARR_REPORTS = [
    'summary_total' => 'Sammendrag',
    // 'sold_out' => 'Utsolgt',
    // 'sales_history' => 'Salgshistorikk',
    // 'qty_for_recent_sales' => 'Salg registrert salg',
  ];

  public function run () {
    $this->page = 'Merke rapport';
    $this->handle_request();
    $this->template->print($this->page);
  }

  private function handle_request () {
    $this->report_type = null;
    $this->brand_id = false;
    if ( isset($_SERVER['REQUEST_URI']) ) {
      $arr = explode('reports/brand/', $_SERVER['REQUEST_URI']);
      if ( isset($arr[1]) ) {
        $arr = explode('/', $arr[1]);
        $this->brand_id = $arr[0];
        if ( isset($arr[1]) ) {
          $arr = explode($this->brand_id, $arr[1]);
          $this->report_type = explode('?', $arr[0])[0];
        }
      }
    }
    if ( is_numeric($this->brand_id) ) {
      $this->get_brand_from_brand_id();
      if ($this->brand === false) {
        $this->template->message('Kunne ikke finne merke med id ' . $this->brand_id);
        $this->print_select_brand_table();
        return;
      }
      if ($this->report_type !== null) {
        // if brand and report selected
        $this->show_report_for_brand();
        return;
      }
      $this->show_report_options_for_brand();
      return;
    }
    $this->print_select_brand_table();
  }

  private function print_select_brand_table () {
    $this->title_left = 'Rapport for utvalgt Merkevare';
    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $query = new QueryReports();
    $query->all_brands();
    $hyperlink_row = new HyperLink();
    $this->database->select_multi_row($query->get());
    if ($this->database->result) {
      $this->template->message('Velg merke ved å klikke på listen');
      $this->template->script_filter_row_button('0', 'Skriv her for å søke ', $auto_focus = true);
      $this->template->table_full_width_start();
      foreach ($this->database->result as $row) {
        $brand = CharacterConvert::iso_8859_1_to_utf_8($row['brand']);
        $hyperlink_row->link_redirect('reports/brand/' . $row['brand_id']);
        $this->template->table_row_start();
        $this->template->table_row_value($brand, $hyperlink_row->url);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }

  private function show_report_options_for_brand () {
    $this->title_left = 'Rapport for ' . $this->brand;
    $this->template->title_left_and_right($this->title_left, $this->title_right);
    $hyperlink_butn = new HyperLink();
    $hyperlink_butn->link_redirect('reports/brand');
    $this->template->hyperlink_button('Tilbake', $hyperlink_butn->url);
    $this->template->line_break();
    $this->template->title('Velg rapport');
    foreach (self::ARR_REPORTS as $name => $alias) {
      $hyperlink_butn->link_redirect('reports/brand/' . $this->brand_id . '/'. $name);
      $this->template->hyperlink_button($alias, $hyperlink_butn->url);
    }
  }

  private function get_brand_from_brand_id () {
    $query = new QueryReports();
    $query->brand_by_brand_id($this->brand_id);
    $this->database->select_single_row($query->get());
    if ($this->database->result) {
      $this->brand = $this->database->result['brand'];
      $this->brand = CharacterConvert::iso_8859_1_to_utf_8($this->brand);
      return;
    }
    $this->brand = false;
  }

  private function show_report_for_brand () {
    $hyperlink_butn = new HyperLink();
    $hyperlink_butn->link_redirect('reports/brand/' . $this->brand_id);

    $this->template->title_left_and_right(self::ARR_REPORTS[$this->report_type] . ' ' . $this->brand, $this->title_right);
    $this->template->hyperlink_button('Tilbake', $hyperlink_butn->url);
    if ($this->date_type == 'calendar') {
      $desc = 'Med aktivitet i tidsrommet ' . $_GET['calendar_from_date'] . ' til og med ' . $_GET['calendar_to_date'];
      $this->template->message($desc);
    } else {
      $this->template->message('Inkludere artikler med aktivitet innenfor valgt dato');
    }
    $this->template->reports_form_input_date();
    if ($this->date_type !== 'calendar') {
      return;
    }
    switch ($this->report_type) {
      case 'summary_total':
        $this->summary_total();
        break;
      case 'sold_out':
        $this->report_sold_out();
        break;
      case 'sales_history':
        $this->report_sales_history();
        break;
      case 'qty_for_recent_sales':
        $this->qty_for_recent_sales();
        break;
      default:
        $this->report_default();
    }
  }

  private function summary_total () {
    $table_headers = [
      'Artikkel' => 'article',
      'På lager' => 'stock_quantity',
      'Salg' => 'sales_total',
      'Siste Salg' => 'lastsold',
      'Varemottak' => 'received_total',
      'Siste mottak' => 'lastimported',
      'Korrigering ' => 'manual_adjustment_total',
      'ABC-kode' => 'abc_code',
      'Siste Lev. ID' => 'supplyid'
    ];
    $spreadsheet_row = array();
    $this->template->script_filter_row_button('0', 'Skriv her for å søke ', $auto_focus = true);
    $hyperlink_toggle = new HyperLink();
    $hyperlink_toggle->add_query('article_status', $this->article_status);
    $this->template->hyperlink_button($this->article_status_message, $hyperlink_toggle->url);
    $this->template->hyperlink_button_target_top('Last ned regneark', $this->hyperlink_spreadsheet->url);
    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $hyperlink_header = new HyperLink();
    foreach ($table_headers as $alias => $name) {
      array_push($spreadsheet_row, $alias);
      $hyperlink_header->add_query('sort', $name);
      $hyperlink_header->add_query('order', $this->order);
      if ($name == $this->sort_by) {
        $alias .= $this->arrow_symbol;
      }
      $this->template->table_row_header($alias, $hyperlink_header->url);
    }
    $this->template->table_row_end();
    array_push($this->spreadsheet_data, $spreadsheet_row);
    $query = new QueryReports();
    $query->brand_full_overview($this->brand_id);
    // $query->print();
    $this->database->select_multi_row($query->get());
    if ($this->database->result) {
      $hyperlink_row = new HyperLink();
      foreach ($this->database->result as $row) {
        $article_id = $row['article_id'];
        $article_name = CharacterConvert::iso_8859_1_to_utf_8($row['article_name']);
        $stock_quantity = $row['stock_quantity'];
        $manual_adjustment_total = $row['manual_adjustment_total'];
        $sales_total = $row['sales_total'];
        $lastsold = $row['lastsold'];
        $received_total = $row['received_total'];
        $lastimported = $row['lastimported'];
        $abc_code = $row['abc_code'];
        $supplyid = $row['supplyid'];
        $hyperlink_row->link_redirect_query('find/articlemovement', 'article_id',  $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value($article_name, $hyperlink_row->url);
        $this->template->table_row_value($stock_quantity);
        $this->template->table_row_value($sales_total);
        $this->template->table_row_value($lastsold);
        $this->template->table_row_value($received_total);
        $this->template->table_row_value($lastimported);
        $this->template->table_row_value($manual_adjustment_total);
        $this->template->table_row_value($abc_code);
        $this->template->table_row_value($supplyid);
        $this->template->table_row_end();
        array_push($this->spreadsheet_data, [$article_name, intval($stock_quantity), intval($sales_total), $lastsold, intval($received_total), $lastimported, intval($manual_adjustment_total), $abc_code, $supplyid]);
      }
    }
    $this->template->table_end();
  }

  private function report_sold_out () {
    $this->template->message('report_sold_out');
  }

  private function report_sales_history () {
    $this->template->message('report_sales_history');
  }

  private function qty_for_recent_sales () {
    $this->template->message('qty_for_recent_sales');
  }
  private function report_default () {
    $this->template->message('default');
  }

}
