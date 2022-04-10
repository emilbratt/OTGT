<?php

require_once '../applications/QueryRetail.php';

class QueryRetailPlacement extends QueryRetail {

  protected $time_span;
  protected $items;
  protected $sort;
  protected $order;

  function __construct () {
    parent::__construct();
  }

  public function basic_article_info_by_ean () {
    $ean = $_POST['barcode'];
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS articleid,
      Article.articleName AS article,
      articleStock.StorageShelf AS location,
      Brands.brandLabel AS brand
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      ArticleEAN ON Article.articleId = ArticleEAN.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    WHERE
      ArticleEAN.eanCode = '$ean'\n
    EOT;
  }

}
