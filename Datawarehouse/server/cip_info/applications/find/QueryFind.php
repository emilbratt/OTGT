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
      'DATABASE', 'DELETE', 'MODIFY', 'UPDATE', 'INSERT', 'DROP', 'KAKE'
    ];

  }

  protected function special_character_replace () {
    $this->query = preg_replace('/(\ø|æ|å|Ø|Æ|Å|tiss)/', '_', $this->query);
  }

  public function print () {
    echo '<pre>';
    echo $this->query;
    echo '</pre>';
  }

  public function get () {
    $this->special_character_replace();
    return $this->query;
  }

}

class QueryFindSearch extends QueryFind {

  public function add_search_brand ($string) {
    // add search for brand
    $this->query .= <<<EOT
    WHERE Brands.brandLabel LIKE '%$string%'\n
    EOT;
  }

  public function add_search_article ($string) {
    // add search for name
    $array = explode(' ', $string);
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


}

class QueryFindBarcode extends QueryFind {

  public function  instantiate () {
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
