<?php

class QueryRetail {

  protected $query;
  protected $template = "SET LANGUAGE NORWEGIAN\n"; // always use norwegian
  protected $illegal_reserved_words; // simple way to prevent script kiddie level sql injection
  protected $special_characters; // mainly to swap "æ", "ø" and "å" to  "_"

  function __construct () {
    $this->illegal_reserved_words = [
      'DATABASE', 'DELETE', 'MODIFY', 'UPDATE', 'INSERT', 'DROP',
    ];
    $this->start_new();
  }

  private function start_new () {
    $this->query = $this->template;
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

  public function update_placement_by_article_id ($article_id, $shelf) {
    $this->query .= <<<EOT
    UPDATE
      articleStock
    SET
      StorageShelf = '$shelf'
    WHERE
      articleStock.articleId = '$article_id'\n
    EOT;
  }

  public function update_placement_by_barcode ($ean, $shelf) {
    $this->query .= <<<EOT
    UPDATE
      articleStock
    SET
      StorageShelf = '$shelf'
    FROM
      articleStock
    JOIN
      ArticleEAN
    ON
      articleStock.articleId = ArticleEAN.articleId
    WHERE
      ArticleEAN.eanCode = '$ean'\n
    EOT;
  }

  public function select_article_id_by_barcode ($ean = false) {
    if ( !(isset($_GET['input_field_barcode'])) or !($ean) ) {
      return;
    }
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS articleid
    FROM
      Article
    INNER JOIN
      ArticleEAN ON Article.articleId = ArticleEAN.articleId
    WHERE
      ArticleEAN.eanCode = '$ean'\n
    EOT;
  }

  public function select_barcodes_by_article_id ($article_id = false) {
    if ( isset($_GET['article_id']) ) {
      $article_id = $_GET['article_id'];
    }
    if ( !($article_id) ) {
      echo 'No article id where passed'; exit(1);
    }
    $this->query .= <<<EOT
    SELECT
      ArticleEAN.eanCode AS barcode,
      ArticleEAN.sysGen AS barcode_is_default
    FROM
      ArticleEAN
    WHERE
      ArticleEAN.articleId = '$article_id'
    ORDER BY
      sysGen desc\n
    EOT;
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
    $article = $_GET['input_field_article'];
    if ($article == '') {
      return;
    }
   /**
    * we split the string by whitespace and add a conditional for each
    * word creating a way to get resaults regardless of where the
    * word originally is positioned by the article we are searching
    */

    $arr_article = explode(' ', $article);
    foreach ($arr_article as $article) {
     /**
      * I dont know how to use prepared statements for an undefined amount
      * of search strings
      *
      * while this is a kind of naive way to secure queries against
      * injection, it is better than nothing at this point..
      *
      * you can for example write DELETE- (notice the hyphen) and it
      * will go unnoticed however, this will never be a public facing
      * service anyways
      */

      $this->check_illegal_word($article);
      if ( $this->has_where() ) {
        $this->query .= <<<EOT
        AND
          Article.articleName LIKE '%$article%'\n
        EOT;
      }
      else {
        $this->query .= <<<EOT
        WHERE
          Article.articleName LIKE '%$article%'\n
        EOT;
      }
    }
  }

  public function where_article_expired () {
    $items = 'all';
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

  public function where_barcode ($force_where = false) {
    $ean = $_GET['input_field_barcode'];
    if ($force_where) {
      // skip checking if WHERE is present in the query (mostly for nested queries with where clause inside)
      $this->query .= <<<EOT
      WHERE
        ArticleEAN.eanCode = '$ean'\n
      EOT;
      return;
    }
    if ( $this->has_where() ) {
      $this->query .= <<<EOT
      AND
        ArticleEAN.eanCode = '$ean'\n
      EOT;
    }
    else {
      $this->query .= <<<EOT
      WHERE
        ArticleEAN.eanCode = '$ean'\n
      EOT;
    }
  }

  public function where_shelf ($force_where = false) {
    $shelf = $_GET['input_field_shelf'];
    $this->check_illegal_word($shelf);
    if ($force_where) {
      // skip checking if WHERE is present in the query (mostly for nested queries with where clause inside)
      $this->query .= <<<EOT
      WHERE
        articleStock.StorageShelf LIKE '$shelf%'\n
      EOT;
      return;
    }
    if ( $this->has_where() ) {
      $this->query .= <<<EOT
      AND
        articleStock.StorageShelf LIKE '$shelf%'\n
      EOT;
    }
    else {
      $this->query .= <<<EOT
      WHERE
        articleStock.StorageShelf LIKE '$shelf%'\n
      EOT;
    }
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

  public function print () {
    // for debugging only (show current query)
    echo '<pre>';
    echo $this->query;
    echo '</pre>';
    die;
  }

  public function get () {
    $this->query = preg_replace('/(\ø|æ|å|Ø|Æ|Å)/', '_', $this->query);
    $query = $this->query;
    $this->start_new();
    return $query;
  }

}
