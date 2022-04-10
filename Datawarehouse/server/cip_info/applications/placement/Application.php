<?php

/**
 *
 * TODO:
 *  add: validate successfull placement update and maybe show history using session_start()
 *  add: when item is scanned, if it already has placement; show it
 *
 */

class Placement {
  // register placement for items
  protected $page = 'Plasser Vare';
  protected $environment;
  protected $template;
  protected $database_retail;
  protected $database_datawarehouse;
  protected $navigation;
  protected $ean;
  protected $message;
  protected $article_id;
  protected $article_id_ok;
  protected $ean_ok;
  protected $shelf;
  protected $shelf_ok;

  function __construct () {
    require_once '../applications/Date.php';
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/QueryRetailPlacement.php';
    require_once '../applications/placement/QueryDatawarehousePlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationPlacement();
    $this->database_retail = new DatabaseRetail();
    $this->template = new TemplatePlacement();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Placement {

    public function run () {
      // step 1: scan item (this form sets placement_scan_item)
      if ( !(isset($_POST['barcode'])) ) {
        $this->placement_scan_item();
        $this->template->message('Det er enkelt å legge inn plassering');
        $this->template->message('Skann en vare først');
        $this->template->message('Deretter skanner du hyllen');
        $this->template->message('Du trenger ikke å bruke mus og tastatur for å gjør dette');
      }
      // step 2: validate item scan and then scan shelf (this form sets both placement_scan_item and placement_scan_shelf)
      else if ( isset($_POST['barcode']) and (!(isset($_POST['shelf']))) ) {
        $this->placement_scan_shelf();
      }
      // step 3: upload new shelf value for item using placement_scan_item and placement_scan_shelf
      else if ( isset($_POST['article_id']) and isset($_POST['shelf']) ) {
        $this->placement_update();
      }

      $this->template->print();
    }

    private function placement_scan_item () {
      $this->template->title('Skann Vare');
      $this->template->form_start('POST');
      $this->template->_form_scan_item();
      $this->template->_form_end();
    }

    private function placement_scan_shelf () {
      $this->ean = $_POST['barcode'];
      $this->validate_barcode();
      if ( !($this->ean_ok) ) {
        $this->placement_scan_item();
        $this->template->message($this->message);
        return;
      }

      $query_retail = new QueryRetailPlacement();
      $query_retail->basic_article_info_by_ean();
      $this->database_retail->select_sinlge_row($query_retail->get());
      if ( !($this->database_retail->result) ) {
        $this->placement_scan_item();
        $this->template->title('Ingen vare med strekkode: ' . $_POST['barcode']);
        return;
      }

      $this->article_id = $this->database_retail->result['articleid'];
      $article = CharacterConvert::utf_to_norwegian($this->database_retail->result['article']);
      $brand = CharacterConvert::utf_to_norwegian($this->database_retail->result['brand']);
      $location = $this->database_retail->result['location'];
      $this->template->title('Skann Hylle');
      $this->template->form_start('POST');
      $this->template->_form_scan_shelf($this->article_id, $article, $brand);
      $this->template->_form_end();
      $this->template->title($brand . ' ' . $article);
      if ( ($location != null) and (strlen($location) > 0) ) {
        $this->template->image_location($location);
        $this->template->title($location);
      }
    }

    private function placement_update () {
      $this->article_id = $_POST['article_id'];
      $this->validate_article_id();
      if ( !($this->article_id_ok)) {
        $this->template->message($this->message);
        return;
      }
      $this->shelf = $_POST['shelf'];
      $this->validate_shelf();
      if ( !($this->shelf_ok) ) {
        $this->placement_scan_shelf();
        $this->template->message($this->message);
        return;
      }
      // at this point, we can update the new shelf value to retial db and datawarehouse db
      $this->update_placement_to_retail();
      $this->insert_placement_to_datawarehouse();
      // re-load the scan item form
      $this->placement_scan_item();
    }

    private function update_placement_to_retail () {
      $query_retail = new QueryRetailPlacement();
      $query_retail->update_placement_by_article_id($this->article_id, $this->shelf);
      $stmt = $this->database_retail->cnxn->prepare($query_retail->get());
      $stmt->execute();
    }

    private function insert_placement_to_datawarehouse () {
      $date_obj = new Date;
      $query_datawarehouse = new QueryDatawarehousePlacement();
      $database_datawarehouse = new DatabaseDatawarehouse();

      $timestamp = $date_obj->timestamp_datawarehouse;
      $yyyymmdd = $date_obj->yyyymmdd;

      $query_datawarehouse->insert_placement();
      $stmt = $database_datawarehouse->cnxn->prepare($query_datawarehouse->get());

      $values = ['article_id' => $this->article_id, 'shelf' => $this->shelf, 'timestamp' => $timestamp, 'yyyymmdd' => $yyyymmdd];
      // since article_id constraint might not have been updated to datawareouse
      // we make a try / exception to handle that specific case
      try {
        $stmt->execute($values);
      }
      catch(PDOException $e)  {
        if (strpos($e, 'Integrity constraint violation') !== false) {
          $this->template->message('Info: denne varen finnes kun i HIP databasen foreløpig');
        }
        else {
          $dev_phone = $this->environment->contact_dev('phone');
          $dev_email = $this->environment->contact_dev('email');
          $dev = $this->environment->contact_dev('name');
          $this->template->title('Noe galt skjedde');
          $this->template->message('Kontakt: ' . $dev);
          $this->template->message('Epost: ' . $dev_email);
          $this->template->message('Telefon: ' .$dev_phone);
          $this->template->message('Og oppgi informasjonen under');
          $this->template->message($e);
          $this->template->print();
          exit(1);
        }
      }

    }

    private function validate_article_id () {
      // this should never error out, but we include it just in case
      $this->article_id_ok = false;
      if ( !(is_numeric($this->article_id)) ) {
        $this->message = 'Artikkel id stemmer ikke, noe galt skjedde<br>';
        $this->message .= 'For hjelp, kontakt<br>';
        $dev_phone = $this->environment->contact_dev('phone');
        $dev_email = $this->environment->contact_dev('email');
        $dev = $this->environment->contact_dev('name');
        $this->message .= 'Utvikler: ' . $dev . '<br>';
        $this->message .= 'Epost: ' . $dev_email . '<br>';
        $this->message .= 'Telefon: ' . $dev_phone;
        return;
      }
    $this->article_id_ok = true;
    }

    private function validate_barcode () {
      $this->ean_ok = false;
      if ( $this->ean == '') {
        $this->message('Tom strekkode');
        return;
      }
      else if (!(is_numeric($this->ean)) ) {
        $this->message = 'Strekkoder kan kun inneholde tall';
        return;
      }
      else if ( strlen($this->ean) < 8 ) {
        $this->message = 'Strekkoder kan ha minimum 8 tall';
        return;
      }
      else if ( strlen($this->ean) > 13 ) {
        $this->message = 'Strekkoder kan ha maksimum 13 tall';
        return;
      }
      $this->ean_ok = true;
    }

    private function validate_shelf () {
      $this->shelf_ok = false;
      // format the shelf value first in case
      $this->shelf = str_replace('+', '-', $this->shelf);
      $this->shelf = strtoupper($this->shelf);
      // then check integrity of the format
      if (strlen($this->shelf) < 1) {
        $this->message = 'Hyllelplass må være minst en karakter';
        return;
      }
      if ( (strlen($this->shelf) == 1) and ($this->shelf == ' ') ) {
        $this->message = 'Hvis du kun skal ha en bokstav så kan det ikke være mellomrom tegn';
        return;
      }
      if (strlen($this->shelf) > 1) {
        if ( !(strpos($this->shelf, '-'))) {
          $this->message = 'Det må brukes bindestrek for å skille mellom lager, hylle og plass<br>';
          $this->message .= 'Eksempel: F-B-10<br>';
          $this->message .= '..hvor F = lager, B = hylle og 10 er plass på hylla<br>';
          $this->message .= 'Tips: du kan også skrive kun F hvis du ikke vil registrere hylle og plass<br>';
          return;
        }
      }
    $this->shelf_ok = true;
    }

}
