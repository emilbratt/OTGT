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

  public function article_id_and_article_name_by_ean () {
    $ean = $_POST['barcode'];
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      Article.articleName AS article
    FROM
      Article
    INNER JOIN
      ArticleEAN ON Article.articleId = ArticleEAN.articleId
    WHERE
      ArticleEAN.eanCode = '$ean'\n
    EOT;
  }

  public function article_brand_and_name_by_article_id ($article_id) {
    $this->query .= <<<EOT
    SELECT
      Article.articleName AS article,
      Brands.brandLabel AS brand
    FROM
      Article
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    WHERE
      Article.articleId = '$article_id'\n
    EOT;
  }

  public function last_imported_items () {
    $this->query .= <<<EOT
    SELECT
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      Article.articleId AS article_id,
      articleStock.StorageShelf AS location
    FROM
      Article
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    WHERE Article.articleId IN
    (
      SELECT articleId
      FROM StockAdjustment
      WHERE adjustmentCode = '41'
      AND DATEPART(WEEK, [adjustmentDate]) = DATEPART(WEEK, CURRENT_TIMESTAMP)
      AND DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, CURRENT_TIMESTAMP)
    )

    ORDER BY
      Brands.brandLabel, Article.articleName\n
    EOT;
  }

}
