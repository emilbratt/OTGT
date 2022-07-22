<?php

require_once '../applications/QueryRetail.php';

class QueryRetailFindBySearch extends QueryRetail {

  function __construct () {
    parent::__construct();
  }

  public function select_fields () {
    $this->query = <<<EOT
    SELECT
      Article.articleId AS article_id,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST (stockQty AS INT) AS quantity,
      articleStock.StorageShelf AS location,
      Article.suppliers_art_no AS supplyid,
      ArticleEAN.eanCode AS barcode
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    INNER JOIN
      ArticleEAN ON Article.articleId = ArticleEAN.articleId
    WHERE
      ArticleEAN.sysGen = '1'\n
    EOT;
  }

}


class QueryRetailFindByArticle extends QueryRetail {

  function __construct () {
    parent::__construct();
  }

  public function select_item_info () {
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
      lastsold
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
      b.b_article_id = Article.ArticleId\n
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
    else if ( isset($_GET['article_id'])) {
      $article_id = $_GET['article_id'];
      $this->query .= <<<EOT
      WHERE
        Article.articleId = '$article_id'\n
      EOT;
    }
  }

}

class QueryRetailFindArticleMovement extends QueryRetail {

  function __construct () {
    parent::__construct();
  }

  public function select_article_movement_summary () {
    if ( isset($_GET['input_field_barcode']) ) {
      $ean = $_GET['input_field_barcode'];
      $where_clause = <<<EOT
          INNER JOIN
            ArticleEAN ON StockAdjustment.articleId = ArticleEAN.articleId
          WHERE
            ArticleEAN.eanCode = '$ean'\n
      EOT;
    }
    else if ( isset($_GET['article_id'])) {
      $article_id = $_GET['article_id'];
      $where_clause = <<<EOT
          WHERE
            StockAdjustment.articleId = '$article_id'\n
      EOT;
    }

    $this->query .= <<<EOT
    SELECT yyyy, movement, SUM(qty) AS qty FROM
    (
      SELECT
        stockAdjustmenId AS stockAdjustmenId,
        adjustmentQty AS qty,
        adjustmentDate AS date,
        YEAR(adjustmentDate) AS yyyy,
        CASE
          WHEN adjustmentCode = '1' THEN 'korreksjon minus'
          WHEN adjustmentCode = '2' THEN 'korreksjon pluss'
          WHEN adjustmentCode = '3' THEN 'telling'
          WHEN adjustmentCode = '4' THEN 'mottak fra bestilling'
          WHEN adjustmentCode = '9' THEN 'salg' -- NOTE: N < 0 = removed from sales header "fjernet fra bong"
          WHEN adjustmentCode = '10' THEN 'kreditering'
          WHEN adjustmentCode = '33' THEN 'tilleggende telling'
          WHEN adjustmentCode = '41' THEN 'varemottak'
          WHEN adjustmentCode = '91' THEN 'intern pakkeseddel el. web-pakkeseddel'
        END AS movement
      FROM
        StockAdjustment
      $where_clause
    ) a
    GROUP BY
      movement, yyyy
    ORDER BY
      yyyy DESC, movement
    EOT;
  }

  public function article_info () {
    if ( isset($_GET['input_field_barcode']) ) {
      $ean = $_GET['input_field_barcode'];
      $where_clause = <<<EOT
      INNER JOIN
        ArticleEAN ON Article.articleId = ArticleEAN.articleId
      WHERE
        ArticleEAN.eanCode = '$ean'\n
      EOT;
    }
    else if ( isset($_GET['article_id'])) {
      $article_id = $_GET['article_id'];
      $where_clause = <<<EOT
      WHERE
        Article.articleId = '$article_id'\n
      EOT;
    }
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST (stockQty AS INT) AS quantity,
      Article.suppliers_art_no AS supplyid
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    $where_clause
    EOT;
  }
}
