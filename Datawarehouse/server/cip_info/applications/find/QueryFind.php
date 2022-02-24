<?php

// the "pages" inside each directory uses this file to get their
// needed sql queries to generate correct reports


class QueryFind {

  protected $query;
  protected $illegal_reserved;
  protected $special_characters;

  function __construct () {
    $this->query = <<<EOT
    SET LANGUAGE NORWEGIAN
    SELECT
      Article.articleId AS articleid,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST (stockQty AS INT) AS quantity,
      articleStock.StorageShelf AS location,
      Article.suppliers_art_no AS supplyid

    FROM
      Article

    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId\n
    EOT;

    $this->illegal_reserved_words = [
      'DATABASE', 'DELETE', 'MODIFY', 'UPDATE', 'INSERT', 'DROP',
    ];

  }

  public function add_toggle_expired () {
    $items = 'active';
    if(isset($_GET['items'])) {
      $items = $_GET['items'];
    }
    switch ($items) {
      case 'all':
        break;
      case 'expired':
        $this->query .= " AND Article.articleName LIKE '[.]%'";
        break;
      case 'active':
        $this->query .= " AND Article.articleName NOT LIKE '[.]%'";
        break;
    }
  }

  protected function special_character_replace () {
    $this->query = preg_replace('/(\ø|æ|å|Ø|Æ|Å|tiss)/', '_', $this->query);
  }

  public function add_sort () {
    $sort = 'brand';
    if(isset($_GET['sort'])) {
      $sort = $_GET['sort'];
    }
    switch ($sort) {
      case 'article':
        $this->query .= ' ORDER BY Article.articleName';
        break;
      case 'brand':
        $this->query .= ' ORDER BY Brands.brandLabel';
        break;
      case 'quantity':
        $this->query .= ' ORDER BY stockQty';
        break;
      case 'location':
        $this->query .= ' ORDER BY articleStock.StorageShelf';
        break;
      case 'supplyid':
        $this->query .= ' ORDER BY Article.suppliers_art_no';
        break;
    }
  }

  public function add_search_brand () {
    // add search for brand
    $string = $_GET['input_field_brand'];
    $this->query .= <<<EOT
    WHERE Brands.brandLabel LIKE '%$string%'\n
    EOT;
  }

  public function add_search_article () {
    // add search for name
    $array = explode(' ', $_GET['input_field_article']);
    foreach ($array as $string) {
      // i dont know how to use prepared statements for any number of
      // multi word search
      // while this is a kind of naive way to secure queries against
      // injection, it is better than nothing at this point
      // you can for example write DELETE- (notice the hyphen) and it
      // willl go unnoticed
      // however, this will never be a public facing service, only local

      if (in_array(strtoupper($string), $this->illegal_reserved_words) ) {
        echo "<p>Ignored illegal reserved word $string</p>";
        return;
      }
      $this->query .= <<<EOT
      AND Article.articleName LIKE '%$string%'\n
      EOT;
    }
  }

  public function add_order () {
    $order = 'ascending';
    if(isset($_GET['order'])) {
      $order = $_GET['order'];
    }
    switch ($order) {
      case 'ascending':
        $this->query .= ' ASC';
        break;
      case 'descending':
        $this->query .= ' DESC';
        break;
    }
  }

  public function print_query () {
    // for debugging only (show current query)
    echo '<pre>';
    echo $this->query;
    echo '</pre>';
    die;
  }

  public function get () {
    $this->special_character_replace();
    return $this->query;
  }

}

class QueryFindBySearch extends QueryFind {

  function __construct () {
    parent::__construct();
  }

}

class QueryFindByBarcode extends QueryFind {

  function __construct () {
    parent::__construct();
    // with the default start of query, we also at this part
    // so that we are able to use barcode in the where clause
    $this->query .= <<<EOT
    INNER JOIN
      ArticleEAN ON Article.articleId = ArticleEAN.articleId
    WHERE
    EOT;
  }


  public function add_barcode ($part) {
    if(!(is_numeric($part))) {
      // barcode should be all numbers
      // also, no sql injection here, this is a simple way to avoid it
      echo "$part is not a barcode";
      exit(1);
    }
    $this->query .= <<<EOT
      ArticleEAN.eanCode = '$part'
    EOT;
  }

  public function prnit () {
    echo $this->qiery;
  }


}
