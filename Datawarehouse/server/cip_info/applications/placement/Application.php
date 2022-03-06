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

      // scan item (this form sets placement_scan_item)
      if ( !(isset($_POST['placement_scan_item'])) ) {
        $this->placement_scan_item();
      }
      // scan shelf (this form sets both placement_scan_item and placement_scan_shelf)
      else if (isset($_POST['placement_scan_item']) and (!(isset($_POST['placement_scan_shelf']))) ) {
        $this->placement_scan_shelf();
      }
      // upload new shelf value for item using placement_scan_item and placement_scan_shelf
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
      $query_validate = new QueryPlacement();
      $query_validate->basic_item_info_by_ean($_POST['placement_scan_item']);
      // $this->query->print();
      $this->database->select_one_row($query_validate->get());
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
      $query_article_id = new QueryPlacement();
      $query_article_id->article_id($_POST['placement_scan_item']);
      $this->database->select_one_row($query_article_id->get());
      if ($this->database->result) {
        $this->article_id = $this->database->result['articleid'];
        $query_update_placement = new QueryPlacement();
        $query_update_placement->update_location_by_article_id($this->article_id, $_POST['placement_scan_shelf']);
        $stmt = $this->database->cnxn->prepare($query_update_placement->get());
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
