<?php


class QueryRetail {
  protected $query;
  protected $illegal_reserved_words; // simple way to prevent script kiddie level sql injection
  protected $special_characters; // mainly to swap æ, ø and å to  _

  function __construct () {
    $this->query = "SET LANGUAGE NORWEGIAN\n"; // always use norwegian

    $this->illegal_reserved_words = [
      'DATABASE', 'DELETE', 'MODIFY', 'UPDATE', 'INSERT', 'DROP', 'KAKE'
    ];

  }

  protected function special_character_replace () {
    $this->query = preg_replace('/(\ø|æ|å|Ø|Æ|Å)/', '_', $this->query);
  }

  protected function check_illegal_word ($string) {
    // we do not want to have words like DROP, DELETE etc. as part of queries
    if (in_array(strtoupper($string), $this->illegal_reserved_words)) {
      echo "<p>Illegal reserved word $string in query</p>";
      $this->print_query();
      exit(1);
    }
  }

  protected function has_where () {
    // check if our query has the reserved word WHERE in it
    return strpos($this->query, 'WHERE') !== false;
  }

  public function where_brand () {
    $string = $_GET['input_field_brand'];
    if ($string == '') {
      return;
    }
    $this->check_illegal_word($string);
    if ( $this->has_where() ) {
      $this->query .= <<<EOT
      AND Brands.brandLabel LIKE '%$string%'\n
      EOT; return;
    }
    $this->query .= <<<EOT
    WHERE Brands.brandLabel LIKE '%$string%'\n
    EOT;
  }

  public function where_article () {
    $string = $_GET['input_field_article'];
    if ($string == '') {
      return;
    }
    // we split the string by whitespace and add a conditional for each
    // word creating a way to get resaults regardless of where the
    // word originally is positioned by the article we are searching
    $array = explode(' ', $string);
    foreach ($array as $string) {
      // i dont know how to use prepared statements for any number of
      // multi word search
      // while this is a kind of naive way to secure queries against
      // injection, it is better than nothing at this point
      // you can for example write DELETE- (notice the hyphen) and it
      // willl go unnoticed
      // however, this will never be a public facing service, only local

      $this->check_illegal_word($string);
      if ( $this->has_where() ) {
        $this->query .= <<<EOT
        AND Article.articleName LIKE '%$string%'\n
        EOT;
      }
      else {
        $this->query .= <<<EOT
        WHERE Article.articleName LIKE '%$string%'\n
        EOT;
      }
    }
  }

  public function where_article_expired () {
    $items = 'active';
    if(isset($_GET['items'])) {
      $items = $_GET['items'];
    }
    switch ($items) {
      case 'all':
        break;
      case 'expired':
        $this->query .= "AND Article.articleName LIKE '[.]%'\n";
        break;
      case 'active':
        $this->query .= "AND Article.articleName NOT LIKE '[.]%'\n";
        break;
    }
  }

  public function where_barcode () {
    $string = $_GET['barcode'];
    if(!(is_numeric($string))) {
      echo "<p>Could not verify that $string is a valid barcode</p>";
      $this->print_query();
    }
    if(!(is_numeric($string))) {
      echo "<p>Could not verify that $string is a valid barcode</p>";
      $this->print_query();
    }
    $this->query .= <<<EOT
      ArticleEAN.eanCode = '$part'
    EOT;
  }

  public function sort_by () {
    $sort = 'brand';
    if(isset($_GET['sort'])) {
      $sort = $_GET['sort'];
    }
    switch ($sort) {
      case 'article':
        $this->query .= 'ORDER BY Article.articleName';
        break;
      case 'brand':
        $this->query .= 'ORDER BY Brands.brandLabel';
        break;
      case 'quantity':
        $this->query .= 'ORDER BY stockQty';
        break;
      case 'location':
        $this->query .= 'ORDER BY articleStock.StorageShelf';
        break;
      case 'supplyid':
        $this->query .= 'ORDER BY Article.suppliers_art_no';
        break;
    }
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
    // $this->print_query(); // comment / uncomment for debugging
    return $this->query;
  }


}
