<?php

// the "pages" inside each directory uses this file to get their
// needed sql queries to generate correct reports


class QuerySoldout {

  public static function get () {
    $query = <<<EOT
    SELECT
      Brands.brandLabel AS Merke,
      Article.articleName AS Navn,
      CAST (stockQty AS INT) AS Antall,
      articleStock.StorageShelf AS Plasserng,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS Sist_Importert,
      Article.suppliers_art_no AS Lev_id
    FROM
      Article
      INNER JOIN articleStock ON Article.articleId = articleStock.articleId
      INNER JOIN Brands ON Article.brandId = Brands.brandId
    WHERE
      ArticleStatus = '0' AND stockQty<='0' AND
      DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP)
    EOT;


    $type = 'today';
    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'today':
        $query .= 'AND DATEPART(DAYOFYEAR, articleStock.lastSold) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)';
        break;
      case 'thisweek':
        $query .= 'AND DATEPART(WEEK, articleStock.lastSold) = DATEPART(WEEK, CURRENT_TIMESTAMP)';
      break;
      case 'thismonth':
        $query .= 'AND DATEPART(MONTH, articleStock.lastSold) = DATEPART(MONTH, CURRENT_TIMESTAMP)';
      break;
    }

    $filter = 'default';
    if(isset($_GET['filter'])) {
      $filter = $_GET['filter'];
    }
    switch ($filter) {
      case 'none':
        $query .= "AND Article.articleName NOT LIKE '[.]%'";
        break;
      case 'expired':
        $query .= "AND Article.articleName LIKE '[.]%'";
        break;
      case 'none-expired':
        $query .= "AND Article.articleName NOT LIKE '[.]%'";
        break;
      case 'default':
        $query .= "AND Article.articleName NOT LIKE '[.]%'";
      default:
        $query .= "AND Article.articleName NOT LIKE '[.]%'";
    }

    $sort = 'default';
    if(isset($_GET['sort'])) {
      $sort = $_GET['sort'];
    }
    switch ($sort) {
      case 'article':
        $query .= 'ORDER BY Article.articleName';
        break;
      case 'brand':
        $query .= 'ORDER BY Brands.brandLabel';
        break;
      case 'quantity':
        $query .= 'ORDER BY stockQty';
        break;
      case 'default':
        $query .= 'ORDER BY articleStock.lastReceivedFromSupplier';
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
