<?php

require_once '../applications/QueryRetail.php';

class QueryRetailFindBySearch extends QueryRetail {

  function __construct () {
    parent::__construct();

    $this->query = <<<EOT
    SELECT
      Article.articleId AS article_id,
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
  }

}


class QueryRetailFindByArticle extends QueryRetail {

  function __construct () {
    parent::__construct();

    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      brand,
      article,
      category,
      price,
      quantity,
      location,
      supplyid,
      lastimported,
      lastsold,
      CASE
        WHEN qty_sold_last_6_months IS NULL THEN 0
        ELSE qty_sold_last_6_months
      END AS qty_sold_last_6_months

    FROM
      Article

    LEFT JOIN
    (
      SELECT
        view_HIP_Productinfo.ArticleId AS a_article_id,
        view_HIP_Productinfo.brandLabel AS brand,
        view_HIP_Productinfo.articleName AS article,
        view_HIP_Productinfo.ArticleGroupName AS category,
        view_HIP_Productinfo.articleUnitPrice AS price,
        view_HIP_Productinfo.supplierId AS Leverandor_id
      FROM
        view_HIP_Productinfo
    )
    a ON
      a.a_article_id = Article.ArticleId

    LEFT JOIN
    (
      SELECT
        Article.ArticleId AS b_article_id,
        articleStock.stockQty AS quantity,
        articleStock.StorageShelf AS location,
        Article.suppliers_art_no AS supplyid,
        CAST(articleStock.lastReceivedFromSupplier AS DATE) AS lastimported,
        CAST(articleStock.lastSold AS DATE) AS lastsold
      FROM
        Article
      INNER JOIN
        articleStock ON Article.articleId = articleStock.articleId
      INNER JOIN
        Brands ON Article.brandId = Brands.brandId
    )
    b ON
      b.b_article_id = Article.ArticleId

    LEFT JOIN
    (
      SELECT
        Article.ArticleId AS c_article_id,
        CAST (SUM(adjustmentQty) AS INT) AS qty_sold_last_6_months
      FROM
        Article
      INNER JOIN
        StockAdjustment ON Article.articleId = StockAdjustment.articleId
      WHERE
        adjustmentCode ='9' AND
        adjustmentDate >= DATEADD(DD, -180, CURRENT_TIMESTAMP)
      GROUP BY Article.ArticleId
    )
    c ON
      c.c_article_id = Article.ArticleId\n
    EOT;

    if ( isset($_GET['input_field_barcode']) ) {
      $ean = $_GET['input_field_barcode'];
      $this->query .= <<<EOT
      INNER JOIN
        ArticleEAN ON Article.articleId = ArticleEAN.articleId
      WHERE
        ArticleEAN.eanCode = '$ean'\n
      EOT;
    }
    if ( isset($_GET['article_id'])) {
      $article_id = $_GET['article_id'];
      $this->query .= <<<EOT
      WHERE
        Article.articleId = '$article_id'\n
      EOT;
    }
  }


}
