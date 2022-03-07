<?php

/**
 *
 * TODO:
 * validate item and shelf value scan input in ScanItemScanShelf
 * validate successfull placement update
 *
 */


class Placement {
  // shows reports of soldout items for today, this week or this month
  protected $page = 'Plassering'; // alias for top_navbar
  protected $environment;
  protected $template;
  protected $database;
  protected $navigation;
  protected $query;
  protected $article_id;
  protected $article_name;
  protected $brand_name;
  protected $ean;
  protected $shelf;

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/Environment.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/QueryPlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationPlacement($this->environment);
    $this->database = new DatabaseRetail($this->environment);
    $this->template = new TemplatePlacement();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Placement {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
  }

}


class ScanItemScanShelf extends Placement {

    public function run () {

      // step 1: scan item (this form sets placement_scan_item)
      if ( !(isset($_POST['placement_scan_item'])) ) {
        $this->placement_scan_item();
      }
      // step 2: validate item scan and then scan shelf (this form sets both placement_scan_item and placement_scan_shelf)
      else if (isset($_POST['placement_scan_item']) and (!(isset($_POST['placement_scan_shelf']))) ) {
        $this->placement_scan_shelf();
      }
      // step 3: upload new shelf value for item using placement_scan_item and placement_scan_shelf
      else if ( isset($_POST['placement_scan_item']) and isset($_POST['placement_scan_shelf']) ) {
        $this->placement_update();
      }

      $this->template->print();
    }

    private function placement_scan_item () {
      $this->template->title('Skann Vare');
      $this->template->form_start('POST');
      $this->template->_form_scan_item();
      $this->template->form_end();
    }

    private function placement_scan_shelf () {
      $query = new QueryPlacement();
      $query->basic_article_info_by_ean($_POST['placement_scan_item']);
      // $this->query->print();
      $this->database->select_sinlge_row($query->get());
      if ($this->database->result) {
        $this->article_id = $this->database->result['articleid'];
        $this->article_name = CharacterConvert::utf_to_norwegian($this->database->result['article']);
        $this->brand_name = CharacterConvert::utf_to_norwegian($this->database->result['brand']);
        $this->template->title('Skann Hylle');
        $this->template->form_start('POST');
        $this->template->_form_scan_shelf($_POST['placement_scan_item']);
        $this->template->form_end();
        $this->template->title($this->brand_name . ' ' . $this->article_name);
      }
      else {
        $this->placement_scan_item();
        $this->template->title('Ingen vare med strekkode: ' . $_POST['placement_scan_item']);
      }

    }

    private function placement_update () {
      $query = new QueryPlacement();
      $query->article_id($_POST['placement_scan_item']);
      $this->database->select_sinlge_row($query->get());
      if ($this->database->result) {
        $this->article_id = $this->database->result['articleid'];
        $query = new QueryPlacement();
        $query->update_location_by_article_id($this->article_id, $_POST['placement_scan_shelf']);
        $stmt = $this->database->cnxn->prepare($query->get());
        $this->template->message('skipping query execution. commented out $stmt->execute(); because not ready yet because need validating of input');
        // $stmt->execute();
      }

      $this->template->title_left_and_right ($_POST['placement_scan_item'], $_POST['placement_scan_shelf']);
      $this->placement_scan_item('placement_scan_item');
    }

}


class GetPlacement extends Placement {

    public function run () {
      $this->template->title('finn vareplassering');
      $this->template->print();
    }

}
