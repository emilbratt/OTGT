<?php

/**
 *
 * for finding items in a convenient fashion
 * searching by brand, article, barcode, category etc,
 *
 */

class Find {

  protected $visitor_url;
  protected $order;
  protected $hyper_link;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/find/FindTemplate.php';
    require_once '../applications/find/FindQuery.php';

    // default is ascending, but we flip the order of rows if ascending is already set
    $this->order = 'ascending';
    if (isset($_GET['order'])) {
      if ($_GET['order'] == 'ascending') {
        $this->order = 'descending';
      }
    }
  }
}

class Home extends Find {

    public function run () {
      echo 'This is Find';
    }
}

class BySearch extends Find {
  public function run () {
    echo 'This is Find->BySearch';

  }
}

class ByBarcode extends Find {
  public function run () {
    echo 'This is Find->ByBarcide';
  }
}
