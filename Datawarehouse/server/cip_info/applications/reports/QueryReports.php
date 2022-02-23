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
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS lastimported,
      CONVERT(VARCHAR(10), articleStock.lastSold, 105) AS lastsold,
      Article.suppliers_art_no AS supplyid
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

    $sort = 'lastsold';
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
      case 'lastsold':
        $query .= ' ORDER BY articleStock.lastSold';
        break;
      case 'lastimported':
        $query .= ' ORDER BY articleStock.lastReceivedFromSupplier';
        break;
      case 'supplyid':
        $query .= ' ORDER BY Article.suppliers_art_no';
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
    SET LANGUAGE NORWEGIAN
    SELECT
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST(StockAdjustment.adjustmentQty AS INT) AS import_qty,
      CAST (stockQty AS INT) AS quantity,
      articleStock.StorageShelf AS location,
      Article.suppliers_art_no AS supplyid,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS lastimported
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
      default:
        $query .= ' AND DATEPART(DAYOFYEAR, [adjustmentDate]) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP) )';
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

    $sort = 'lastimported';
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
      case 'importquantity':
        $query .= ' ORDER BY StockAdjustment.adjustmentQty';
        break;
      case 'lastimported':
        $query .= ' ORDER BY lastimported';
        break;
      case 'supplyid':
        $query .= ' ORDER BY supplyid';
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


class QuerySold {

  public static function get ($type) {
    $query = <<<EOT
    SELECT
      hipUser.userFirstName AS name,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST(CustomerSales.noOfArticles AS INT) AS soldqty,
    EOT;

    $_date = 'CONVERT(VARCHAR(5), CustomerSaleHeader.salesDate, 8) AS salesdate,';
    if(isset($_GET['type'])) {
      if($_GET['type'] != 'thisday') {
        $_date .= 'CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 105) AS salesdate,';
      }
    }
    $query .= $_date;
    $query .= <<<EOT
      CustomerSales.usedPricePerUnit AS price,
      CustomerSales.disCount AS discount,
      CustomerSaleHeader.additionalInfo AS paymentmethod,
      Article.suppliers_art_no AS supplyid

    FROM
      CustomerSales

    FULL JOIN Article
      ON CustomerSales.articleId = Article.articleId
    FULL JOIN CustomerSaleHeader
      ON CustomerSales.customerSaleHeaderId = CustomerSaleHeader.customerSaleHeaderId
    FULL JOIN Brands
      ON Brands.brandId = Article.brandId
    FULL JOIN hipUser
      ON CustomerSaleHeader.userId = hipUser.userId

    WHERE
      Article.articleId IS NOT NULL AND
      DATEPART(YEAR, CustomerSaleHeader.salesDate) = DATEPART(YEAR, CURRENT_TIMESTAMP)

    EOT;


    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'thisday':
        $query .= ' AND DATEPART(DAYOFYEAR, CustomerSaleHeader.salesDate) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)';
        break;
      case 'thisweek':
        $query .= ' AND DATEPART(WEEK, CustomerSaleHeader.salesDate) = DATEPART(WEEK, CURRENT_TIMESTAMP)';
      break;
      case 'thismonth':
        $query .= ' AND DATEPART(MONTH, CustomerSaleHeader.salesDate) = DATEPART(MONTH, CURRENT_TIMESTAMP)';
      break;
      default:
        $query .= ' AND DATEPART(DAYOFYEAR, CustomerSaleHeader.salesDate) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)';
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

    $sort = 'salesdate';
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
      case 'salesdate':
        $query .= ' ORDER BY CustomerSaleHeader.salesDate';
        break;
      case 'supplyid':
        $query .= ' ORDER BY Article.suppliers_art_no';
      case 'price':
        $query .= ' ORDER BY customerSales.usedPricePerUnit';
        break;
      case 'discount':
        $query .= ' ORDER BY CustomerSales.disCount';
        break;
      case 'paymentmethod':
        $query .= ' ORDER BY CustomerSaleHeader.additionalInfo';
        break;
      case 'name':
        $query .= ' ORDER BY hipUser.userFirstName';
        break;
      case 'soldqty':
        $query .= ' ORDER BY CustomerSales.noOfArticles';
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
