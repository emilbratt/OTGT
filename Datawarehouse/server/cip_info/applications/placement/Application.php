<?php

class Placement {

  protected $page = 'Plassering';
  protected $environment;
  protected $template;
  protected $database_retail;
  protected $database_datawarehouse;
  protected $navigation;
  protected $ean;
  protected $message;
  protected $article_id;
  protected $shelf;
  protected $is_shelf;
  protected $is_ean;
  protected $date_time;
  protected $yyyymmdd;

  function __construct () {
    // session is used to store previously fetched multiple items
    session_start();

    require_once '../applications/Date.php';
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/QueryRetailPlacement.php';
    require_once '../applications/placement/QueryDatawarehousePlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationPlacement();
    $this->database_retail = new DatabaseRetail();
    $this->database_datawarehouse = new DatabaseDatawarehouse();
    $this->template = new TemplatePlacement();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Placement {

  public function run () {
    $hyperlink = new HyperLink();
    $hyperlink->link_redirect('placement/fromimported');
    $this->template->hyperlink_button('Legg inn fra Mottak', $hyperlink->url);
    $hyperlink->link_redirect('placement/newestplacements');
    $this->template->hyperlink_button('Nye plasseringer', $hyperlink->url);

    $this->template->line_break(2);
    $this->template->form_start('POST');
    $this->template->_form_scan_item();
    $this->template->_form_end();

    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
      // GET request means we have not scanned any items and thus show instruction
      $this->template->title('Registrer vareplassering');
      $this->template->message('Start med å skanne en eller flere varer');
      $this->template->message('Etterpå så skanner du hyllemerking');
      // we also remove the articles just in case user has navigated in and out
      unset($_SESSION['articles']);
    }
    else if ($_SERVER['REQUEST_METHOD'] === 'POST') {
      // POST request means we have scanned a barcode
      if ( isset($_POST['barcode']) ) {
        $this->handle_barcode();
      }
    }

    if (isset($_SESSION['articles'])) {
      $this->print_scanned_items();
      $this->template->message('Skann hyllemerking for å legge inn plassering på alle varer over');
    }

    $this->template->print($this->page);
  }

  private function handle_barcode () {
    // first we check if it is an ean
    $this->confirm_ean();
    if ($this->is_ean) {
      $this->add_item_to_session();
      return;
    }
    // second, we check if it is a shelf
    $this->confirm_shelf();
    if ($this->is_shelf) {
      $this->update_database();
      return;
    }
    $this->template->message($this->message);
    // lastly, if none above, nothing to do
  }

  private function confirm_ean() {
    $this->is_ean = false;
    if ( $_POST['barcode'] == '') {
      $this->message = 'Tom strekkode';
      return;
    }
    else if ( !(is_numeric($_POST['barcode'])) ) {
      $this->message = 'Strekkoder kan kun inneholde tall';
      return;
    }
    else if ( strlen($_POST['barcode']) < 8 ) {
      $this->message = 'Strekkoder kan ha minimum 8 tall';
      return;
    }
    else if ( strlen($_POST['barcode']) > 13 ) {
      $this->message = 'Strekkoder kan ha maksimum 13 tall';
      return;
    }
    $this->is_ean = true;
  }

  private function confirm_shelf () {
    $this->shelf = $_POST['barcode'];
    $this->is_shelf = false;
    // swap out de-limitters to "-" (currently allow "+", " ", and ".")
    $this->shelf = str_replace('+', '-', $this->shelf);
    $this->shelf = str_replace(' ', '-', $this->shelf);
    $this->shelf = str_replace('.', '-', $this->shelf);
    $this->shelf = str_replace(',', '-', $this->shelf);
    $this->shelf = strtoupper($this->shelf);
    // if empty
    if (strlen($this->shelf) < 1) {
      $this->message = 'Hyllemerking inneholder ingen karakterer';
      return;
    }
    // if whitespace
    if ($this->shelf == ' ') {
      $this->message = 'Hyllemerking er tom';
      return;
    }
    // if character but no hyphen
    if (strlen($this->shelf) > 1) {
      if ( !(strpos($this->shelf, '-'))) {
        $this->message = 'Hyllemerking er lengre enn 1 karakter og har ikke bindestrek';
        return;
      }
    }
    $this->is_shelf = true;
  }

  private function add_item_to_session () {
    // takes barcode from $_POST['barcode'] and gets article id and article name
    $query_retail = new QueryRetailPlacement();
    $query_retail->article_id_and_article_name_by_ean();
    $this->database_retail->select_single_row($query_retail->get());
    if ( !($this->database_retail->result) ) {
      return;
    }
    // to append to the array, make sure it exists (on first run it most likely does not)
    if ( !(isset($_SESSION['articles'])) ) {
      $_SESSION['articles'] = array();
    }
    $id = $this->database_retail->result['article_id'];
    $name = CharacterConvert::iso_8859_1_to_utf_8($this->database_retail->result['article']);
    $_SESSION['articles'][$_POST['barcode']] = ['id' => $id, 'name' => $name];
  }

  private function print_scanned_items () {
    $this->template->title('Varer skannet hittil');
    $this->template->table_full_width_start();
    $this->template->table_row_start();
    $this->template->table_row_value('<strong>Strekkode</strong>');
    $this->template->table_row_value('<strong>Artikkel</strong>');
    $this->template->table_row_end();
    foreach($_SESSION['articles'] as $barcode => $arr) {
      $this->template->table_row_start();
      $this->template->table_row_value($barcode);
      $this->template->table_row_value($arr['name']);
      $this->template->table_row_end();
    }
    $this->template->table_end();
  }

  private function update_database () {
    if ( !(isset($_SESSION['articles'])) ) {
      return;
    }
    $date_obj = new Date;
    $this->date_time = $date_obj->date_time;
    $this->yyyymmdd = $date_obj->yyyymmdd;
    foreach($_SESSION['articles'] as $barcode => $arr) {
      $this->article_id = $arr['id'];
      $this->placement_to_retail_db();
      $this->placement_to_datawarehouse_db();
    }
    unset($_SESSION['articles']);
    $this->template->message('Varer oppdatert med plassering ' . $this->shelf);
    $this->template->message('Du kan fortsette med å skanne nye varer');
  }

  private function placement_to_retail_db () {
    $query = new QueryRetailPlacement();
    $query->update_placement_by_article_id($this->article_id, $this->shelf);
    $stmt = $this->database_retail->cnxn->prepare($query->get());
    $stmt->execute();
  }

  private function placement_to_datawarehouse_db () {
    // these values go into the database
    $values = [
      'article_id' => $this->article_id,
      'shelf' => $this->shelf,
      'timestamp' => $this->date_time,
      'yyyymmdd' => $this->yyyymmdd
    ];

    // first, try to do an update of timestamp (works if placement exists)
    $query= new QueryDatawarehousePlacement();
    $query->update_timestamp_for_placement();
    $stmt = $this->database_datawarehouse->cnxn->prepare($query->get());
    $stmt->execute($values);
    $this->data['database_datawarehouse'] = true;
    if ($stmt->rowCount() > 0) {
      // affected rows means record exists and timestamp update succeeded
      return;
    }

    // if this block runs, it means we need to insert a new record
    $query->insert_placement();
    $stmt = $this->database_datawarehouse->cnxn->prepare($query->get());
    $stmt->execute($values);
    $this->data['database_datawarehouse'] = true;
  }

}


class FromImported extends Placement {

  public function run () {
    $hyperlink = new HyperLink();
    $hyperlink->link_redirect('placement');
    $this->template->hyperlink_button('Tilbake', $hyperlink->url);
    $hyperlink->link_redirect('placement/fromimported');
    $this->template->hyperlink_button('Last inn på nytt', $hyperlink->url);
    $this->list_newest_imported_items();
    $this->template->print($this->page);
  }

  private function list_newest_imported_items () {
    // this will also allow for changing/updating item plcaement
    $query_retail = new QueryRetailPlacement();
    $query_retail->last_imported_items();
    $this->database_retail->select_multi_row($query_retail->get());
    if ($this->database_retail->result) {
      $hyperlink_row = new HyperLink();
      $this->template->title('Varermottak denne uken');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_header('Merke');
      $this->template->table_row_header('Artikkel');
      $this->template->table_row_header('Plassering');
      $this->template->table_row_end();
      foreach ($this->database_retail->result as $row) {
        $article_id = $row['article_id'];
        $hyperlink_row->link_redirect_query('find/byarticle', 'article_id', $article_id);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($row['brand']));
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($row['article']));
        $this->template->table_row_value_update_location_input($row['location'], $article_id);
        $this->template->table_row_end();
      }
      $this->template->table_end();
      $this->template->script_table_row_value_update_location_input();
    }
    else {
      $this->template->message('Ingen varer har kommet inn i denne uken');
    }
  }
}


class NewestPlacements extends Placement {

  public function run () {
    $hyperlink = new HyperLink();
    $hyperlink->link_redirect('placement');
    $this->template->hyperlink_button('Tilbake', $hyperlink->url);
    $hyperlink->link_redirect('placement/newestplacements');
    $this->template->hyperlink_button('Last inn på nytt', $hyperlink->url);
    $this->show_latest_placements();
    $this->template->print($this->page);
  }

  private function show_latest_placements () {
    $query_datawarehouse = new QueryDatawarehousePlacement();
    $limit = '100';
    $query_datawarehouse->latest_registered_placements($limit);
    $this->database_datawarehouse->select_multi_row($query_datawarehouse->get());
    if ($this->database_datawarehouse->result) {
      $hyperlink = new HyperLink();
      $this->template->title('Nyeste registrerte plasseringer');
      $this->template->table_start();
      $this->template->table_row_start();
      $this->template->table_row_header('Merke');
      $this->template->table_row_header('Artikkel');
      $this->template->table_row_header('Plassering');
      $this->template->table_row_header('Tid');
      $this->template->table_row_end();
      foreach ($this->database_datawarehouse->result as $row) {
        $article = '';
        $brand = '';
        $query_retail = new QueryRetailPlacement();
        $query_retail->article_brand_and_name_by_article_id($row['article_id']);
        $this->database_retail = new DatabaseRetail();
        $this->database_retail->select_single_row($query_retail->get());
        if ($this->database_retail->result) {
          $article = $this->database_retail->result['article'];
          $brand = $this->database_retail->result['brand'];
        }
        $this->database_retail = null;
        $query_retail = null;
        $hyperlink->link_redirect_query('find/byarticle', 'article_id', $row['article_id']);
        $this->template->table_row_start();
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($brand), $hyperlink->url);
        $this->template->table_row_value(CharacterConvert::iso_8859_1_to_utf_8($article), $hyperlink->url);
        $this->template->table_row_value($row['stock_location'], $hyperlink->url);
        $this->template->table_row_value($row['format_timestamp'], $hyperlink->url);
        $this->template->table_row_end();
      }
      $this->template->table_end();
    }
  }
}
