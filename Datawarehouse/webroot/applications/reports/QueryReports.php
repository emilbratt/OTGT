<?php

// the "pages" inside each directory uses this file to get their
// needed sql queries to generate correct reports


class QuerySoldout {

  public static function get ($type) {
    $query = <<<EOT
    SET LANGUAGE NORWEGIAN
    SELECT
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST (stockQty AS INT) AS quantity,
      articleStock.StorageShelf AS location,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS last_imported,
      Article.suppliers_art_no AS supply_id
    FROM
      Article
      INNER JOIN articleStock ON Article.articleId = articleStock.articleId
      INNER JOIN Brands ON Article.brandId = Brands.brandId
    WHERE
      ArticleStatus = '0' AND stockQty <= '0'
      AND DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP)
    EOT;

    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'thisday':
        $query .= ' AND DATEPART(DAYOFYEAR, articleStock.lastSold) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)';
        break;
      case 'thisweek':
        $query .= ' AND DATEPART(WEEK, articleStock.lastSold) = DATEPART(WEEK, CURRENT_TIMESTAMP)';
      break;
      case 'thismonth':
        $query .= ' AND DATEPART(MONTH, articleStock.lastSold) = DATEPART(MONTH, CURRENT_TIMESTAMP)';
      break;
    }

    $items = 'all';
    if(isset($_GET['items'])) {
      $items = $_GET['items'];
    }
    switch ($items) {
      case 'all':
        break;
      case 'expired':
        $query .= " AND Article.articleName LIKE '[.]%'";
        break;
      case 'none-expired':
        $query .= " AND Article.articleName NOT LIKE '[.]%'";
        break;
    }

    $sort = 'sold';
    if(isset($_GET['sort'])) {
      $sort = $_GET['sort'];
    }
    switch ($sort) {
      case 'article':
        $query .= ' ORDER BY Article.articleName';
        break;
      case 'brand':
        $query .= ' ORDER BY Brands.brandLabel';
        break;
      case 'quantity':
        $query .= ' ORDER BY stockQty';
        break;
      case 'location':
        $query .= ' ORDER BY articleStock.StorageShelf';
        break;
      case 'sold':
        $query .= ' ORDER BY articleStock.lastSold';
        break;
    }

    $order = 'ascending';
    if(isset($_GET['order'])) {
      $order = $_GET['order'];
    }
    switch ($order) {
      case 'ascending':
        $query .= ' ASC';
        break;
      case 'descending':
        $query .= ' DESC';
        break;
    }

    return $query;
  }
}


class QueryImported {

  public static function get ($type) {
    $query = <<<EOT
    SELECT
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST(StockAdjustment.adjustmentQty AS INT) AS import_qty,
      CAST (stockQty AS INT) AS quantity,
      articleStock.StorageShelf AS location,
      Article.suppliers_art_no AS supply_id,
      CAST(StockAdjustment.adjustmentDate AS Date) AS last_imported
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    INNER JOIN
      StockAdjustment ON Article.articleId = StockAdjustment.articleId
    WHERE EXISTS
    (
      SELECT
        articleId,
        stockAdjustmenId,
        adjustmentDate
      FROM
        StockAdjustment AS Stock_Ad
      WHERE
        adjustmentCode ='41'
        AND Stock_Ad.articleId = Article.articleId
        AND Stock_Ad.stockAdjustmenId = StockAdjustment.stockAdjustmenId
        AND Stock_Ad.adjustmentDate = StockAdjustment.adjustmentDate
        AND DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, CURRENT_TIMESTAMP)
    EOT;

    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'thisday':
        $query .= ' AND DATEPART(DAYOFYEAR, [adjustmentDate]) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP) )';
        break;
      case 'thisweek':
        $query .= ' AND DATEPART(WEEK, [adjustmentDate]) = DATEPART(WEEK, CURRENT_TIMESTAMP) )';
      break;
      case 'thismonth':
        $query .= ' AND DATEPART(MONTH, [adjustmentDate]) = DATEPART(MONTH, CURRENT_TIMESTAMP) )';
      break;
    }

    $items = 'all';
    if(isset($_GET['items'])) {
      $items = $_GET['items'];
    }
    switch ($items) {
      case 'all':
        break;
      case 'expired':
        $query .= " AND Article.articleName LIKE '[.]%'";
        break;
      case 'none-expired':
        $query .= " AND Article.articleName NOT LIKE '[.]%'";
        break;
    }

    $sort = 'last_imported';
    if(isset($_GET['sort'])) {
      $sort = $_GET['sort'];
    }
    switch ($sort) {
      case 'article':
        $query .= ' ORDER BY article';
        break;
      case 'brand':
        $query .= ' ORDER BY brand';
        break;
      case 'quantity':
        $query .= ' ORDER BY quantity';
        break;
      case 'location':
        $query .= ' ORDER BY location';
        break;
      case 'last_imported':
        $query .= ' ORDER BY last_imported';
        break;
    }

    $order = 'ascending';
    if(isset($_GET['order'])) {
      $order = $_GET['order'];
    }
    switch ($order) {
      case 'ascending':
        $query .= ' ASC';
        break;
      case 'descending':
        $query .= ' DESC';
        break;
    }

    return $query;
  }
}
