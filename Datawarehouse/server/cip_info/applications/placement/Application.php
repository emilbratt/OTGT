<?php

/**
 *
 * TODO:
 *  add: validate item and shelf value scan input in ScanItemScanShelf
 *  add: validate successfull placement update
 *  add: show latest registered placement for articles
 *  add: string to uppercase when storing shelf value
 */


class Placement {
  // shows reports of soldout items for today, this week or this month
  protected $page = 'Plassering'; // alias for top_navbar
  protected $environment;
  protected $template;
  protected $database;
  protected $navigation;
  protected $query;
  protected $ean;
  protected $message;
  protected $article_id;
  protected $article_id_ok;
  protected $ean_ok;
  protected $shelf;
  protected $shelf_ok;


  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/QueryPlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationPlacement();
    $this->database = new DatabaseRetail();
    $this->template = new TemplatePlacement();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Placement {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->message('det kommer flere funksjoner her etter hvert');
    $this->template->print();
  }

}


class ScanItemScanShelf extends Placement {

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

      $query = new QueryPlacement();
      $query->basic_article_info_by_ean();
      // $this->query->print();
      $this->database->select_sinlge_row($query->get());
      if ( !($this->database->result) ) {
        $this->placement_scan_item();
        $this->template->title('Ingen vare med strekkode: ' . $_POST['barcode']);
        return;
      }

      $article_id = $this->database->result['articleid'];
      $article = CharacterConvert::utf_to_norwegian($this->database->result['article']);
      $brand = CharacterConvert::utf_to_norwegian($this->database->result['brand']);
      $this->template->title('Skann Hylle');
      $this->template->form_start('POST');
      $this->template->_form_scan_shelf($article_id, $article, $brand);
      $this->template->_form_end();
      $this->template->title($brand . ' ' . $article);
    }

    private function placement_update () {
      $article_id = $_POST['article_id'];
      $this->shelf = $_POST['shelf'];
      $this->validate_shelf();
      if ( !($this->shelf_ok) ) {
        $this->placement_scan_shelf();
        $this->template->message($this->message);
        return;
      }

      $query = new QueryPlacement();
      $query->update_placement_by_article_id($article_id, $this->shelf);
      $query->print(); die;
      $stmt = $this->database->cnxn->prepare($query->get());
      $this->placement_scan_item('placement_scan_item');
      $this->template->message('skipping query execution. commented out $stmt->execute(); because not ready yet because need validating of input');
      // $stmt->execute();
      return;

      $this->placement_scan_item('placement_scan_item');
    }

    private function validate_article_id () {

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
      if (strlen($this->shelf) < 1) {
        $this->message = 'Hyllelplass må være minst en karakter';
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


class GetPlacement extends Placement {

    public function run () {
      $this->template->title('finn vareplassering');
      $this->template->print();
    }

}
