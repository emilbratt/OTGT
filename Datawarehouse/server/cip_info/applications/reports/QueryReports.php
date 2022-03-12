<?php

require_once '../applications/QueryRetail.php';

class QueryReports extends QueryRetail {

  protected $time_span;
  protected $date_part;
  protected $items;
  protected $sort;
  protected $order;

  function __construct () {
    parent::__construct();

    $this->time_span = 'thisday';
    if(isset($_GET['type'])) {
      $this->time_span = $_GET['type'];
    }
    $this->items = 'all';
    if(isset($_GET['items'])) {
      $this->items = $_GET['items'];
    }
    $this->order = 'ascending';
    if(isset($_GET['order'])) {
      $this->order = $_GET['order'];
    }
    $this->date_part_type = 'year';
    if(isset($_GET['input_field_date_part_type'])) {
      $this->date_part_type = $_GET['input_field_date_part_type'];
    }
  }

  public function sold_out () {
    $this->query .= <<<EOT
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
      ArticleStatus = '0' AND stockQty <= '0'\n
    EOT;

    switch ($this->time_span) {
      case 'thisday':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(DAYOFYEAR, articleStock.lastSold) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thisweek':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(WEEK, articleStock.lastSold) = DATEPART(WEEK, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thismonth':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(MONTH, articleStock.lastSold) = DATEPART(MONTH, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      default:
        if (strtotime($this->time_span)) {
          $_year = date('Y', strtotime($this->time_span));
          $_month = date('m', strtotime($this->time_span));
          $_day = date('d', strtotime($this->time_span));
          $this->query .= <<<EOT
            AND DATEPART(YEAR, articleStock.lastSold) = $_year
            AND DATEPART(MONTH, articleStock.lastSold) = $_month
            AND DATEPART(DAY, articleStock.lastSold) = $_day\n
          EOT;
        }
    }

    switch ($this->items) {
      case 'all':
        break;
      case 'expired':
        $this->query .= <<<EOT
          AND Article.articleName LIKE '[.]%'\n
        EOT;
        break;
      case 'none-expired':
        $this->query .= <<<EOT
          AND Article.articleName NOT LIKE '[.]%'\n
        EOT;
        break;
    }

    $this->sort = 'lastsold';
    if(isset($_GET['sort'])) {
      $this->sort = $_GET['sort'];
    }
    switch ($this->sort) {
      case 'article':
        $string_sort = 'Article.articleName';
        break;
      case 'brand':
        $string_sort = 'Brands.brandLabel';
        break;
      case 'quantity':
        $string_sort = 'stockQty';
        break;
      case 'location':
        $string_sort = 'articleStock.StorageShelf';
        break;
      case 'lastsold':
        $string_sort = 'articleStock.lastSold';
        break;
      case 'lastimported':
        $string_sort = 'articleStock.lastReceivedFromSupplier';
        break;
      case 'supplyid':
        $string_sort = 'Article.suppliers_art_no';
        break;
    }
    switch ($this->order) {
      case 'ascending':
        $string_order = 'ASC';
        break;
      case 'descending':
        $string_order = 'DESC';
        break;
    }
    $this->query .= <<<EOT
    ORDER BY $string_sort $string_order\n
    EOT;
  }

  public function imported () {
    $this->query .= <<<EOT
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
        AND Stock_Ad.adjustmentDate = StockAdjustment.adjustmentDate\n
    EOT;

    switch ($this->items) {
      case 'all':
        break;
      case 'expired':
        $this->query .= <<<EOT
          AND Article.articleName LIKE '[.]%'\n
        EOT;
        break;
      case 'none-expired':
        $this->query .= <<<EOT
          AND Article.articleName NOT LIKE '[.]%'\n
        EOT;
        break;
    }

    switch ($this->time_span) {
      case 'thisday':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(DAYOFYEAR, [adjustmentDate]) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thisweek':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(WEEK, [adjustmentDate]) = DATEPART(WEEK, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thismonth':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(MONTH, [adjustmentDate]) = DATEPART(MONTH, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      default:
        if (strtotime($this->time_span)) {
          $_year = date('Y', strtotime($this->time_span));
          $_month = date('m', strtotime($this->time_span));
          $_day = date('d', strtotime($this->time_span));
          $this->query .= <<<EOT
            AND DATEPART(YEAR, [adjustmentDate]) = $_year
            AND DATEPART(MONTH, [adjustmentDate]) = $_month
            AND DATEPART(DAY, [adjustmentDate]) = $_day\n
          EOT;
        }
    }
    $this->query .= ")\n";

    $this->sort = 'lastimported';
    if(isset($_GET['sort'])) {
      $this->sort = $_GET['sort'];
    }

    switch ($this->sort) {
      case 'article':
        $string_sort = 'article';
        break;
      case 'brand':
        $string_sort = 'brand';
        break;
      case 'quantity':
        $string_sort = 'quantity';
        break;
      case 'location':
        $string_sort = 'location';
        break;
      case 'importquantity':
        $string_sort = 'StockAdjustment.adjustmentQty';
        break;
      case 'lastimported':
        $string_sort = 'lastimported';
        break;
      case 'supplyid':
        $string_sort = 'supplyid';
        break;
    }
    switch ($this->order) {
      case 'ascending':
        $string_order = 'ASC';
        break;
      case 'descending':
        $string_order = 'DESC';
        break;
    }
    $this->query .= <<<EOT
    ORDER BY $string_sort $string_order\n
    EOT;
  }

  public function sold () {
    $this->query .= <<<EOT
    SELECT
      hipUser.userFirstName AS name,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST(CustomerSales.noOfArticles AS INT) AS soldqty,\n
    EOT;
    $_date = 'CONVERT(VARCHAR(5), CustomerSaleHeader.salesDate, 8) AS salesdate,';
    if($this->time_span != 'thisday') {
      $_date = 'CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 105) AS salesdate,';
    }
    $this->query .= <<<EOT
      $_date
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
      Article.articleId IS NOT NULL\n
    EOT;

    switch ($this->time_span) {
      case 'thisday':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, CustomerSaleHeader.salesDate) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(DAYOFYEAR, CustomerSaleHeader.salesDate) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thisweek':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, CustomerSaleHeader.salesDate) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(WEEK, CustomerSaleHeader.salesDate) = DATEPART(WEEK, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thismonth':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, CustomerSaleHeader.salesDate) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(MONTH, CustomerSaleHeader.salesDate) = DATEPART(MONTH, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      default:
        if (strtotime($this->time_span)) {
          $_year = date('Y', strtotime($this->time_span));
          $_month = date('m', strtotime($this->time_span));
          $_day = date('d', strtotime($this->time_span));
          $this->query .= <<<EOT
            AND DATEPART(YEAR, CustomerSaleHeader.salesDate) = $_year
            AND DATEPART(MONTH, CustomerSaleHeader.salesDate) = $_month
            AND DATEPART(DAY, CustomerSaleHeader.salesDate) = $_day\n
          EOT;
        }
    }

    switch ($this->items) {
      case 'all':
        break;
      case 'expired':
        $this->query .= <<<EOT
          AND Article.articleName LIKE '[.]%'\n
        EOT;
        break;
      case 'none-expired':
        $this->query .= <<<EOT
          AND Article.articleName NOT LIKE '[.]%'\n
        EOT;
        break;
    }

    $this->sort = 'salesdate';
    if(isset($_GET['sort'])) {
      $this->sort = $_GET['sort'];
    }
    switch ($this->sort) {
      case 'article':
        $string_sort = 'Article.articleName';
        break;
      case 'brand':
        $string_sort = 'Brands.brandLabel';
        break;
      case 'salesdate':
        $string_sort = 'CustomerSaleHeader.salesDate';
        break;
      case 'supplyid':
        $string_sort = 'Article.suppliers_art_no';
      case 'price':
        $string_sort = 'customerSales.usedPricePerUnit';
        break;
      case 'discount':
        $string_sort = 'CustomerSales.disCount';
        break;
      case 'paymentmethod':
        $string_sort = 'CustomerSaleHeader.additionalInfo';
        break;
      case 'name':
        $string_sort = 'hipUser.userFirstName';
        break;
      case 'soldqty':
        $string_sort = 'CustomerSales.noOfArticles';
        break;
    }
    switch ($this->order) {
      case 'ascending':
        $string_order = 'ASC';
        break;
      case 'descending':
        $string_order = 'DESC';
        break;
    }
    $this->query .= <<<EOT
    ORDER BY $string_sort $string_order\n
    EOT;
  }

  public function in_stock_not_sold_lately () {
    $this->order = 'descending';
    $brand = $_GET['input_field_brand'];
    $location = $_GET['input_field_location'];
    $num_year = $_GET['input_field_date_part_num'];
    $stock_operator = $_GET['input_field_stock_operator'];
    $date_part_type = $_GET['input_field_date_part_type'];
    $stock_limit = $_GET['input_field_stock_num'];
    $this->query .= <<<EOT
    SELECT
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CONVERT(VARCHAR(10), articleStock.lastSold, 23) AS lastsold,
      articleStock.stockQty AS quantity,
      articleStock.StorageShelf AS location,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS lastimported,
      Article.suppliers_art_no AS supplyid

    FROM
      Article

    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId

    WHERE
      articleStock.lastSold < DATEADD($this->date_part_type, -$num_year, CURRENT_TIMESTAMP)
      AND articleStock.stockQty $stock_operator '$stock_limit'
      /**
       *  optionally, we could use datepart and set a fixed year like so (uncommented for now)
       *  AND DATEPART(YEAR, articleStock.lastSold) < DATEPART(YEAR, '2021') -- DATEADD(YEAR, -1, CURRENT_TIMESTAMP)
       */\n
    EOT;
    if ($location !== '') {
      $this->query .= <<<EOT
      AND articleStock.StorageShelf LIKE '$location%'
      EOT;
    }
    if ($brand !== '') {
      $this->query .= <<<EOT
      AND Brands.brandLabel LIKE '%$brand%'
      EOT;
    }
    $this->sort = 'lastsold';
    if(isset($_GET['sort'])) {
      $this->sort = $_GET['sort'];
    }
    switch ($this->sort) {
      case 'article':
        $string_sort = 'Article.articleName';
        break;
      case 'brand':
        $string_sort = 'Brands.brandLabel';
        break;
      case 'quantity':
        $string_sort = 'stockQty';
        break;
      case 'location':
        $string_sort = 'articleStock.StorageShelf';
        break;
      case 'lastsold':
        $string_sort = 'articleStock.lastSold';
        break;
      case 'lastimported':
        $string_sort = 'articleStock.lastReceivedFromSupplier';
        break;
      case 'supplyid':
        $string_sort = 'Article.suppliers_art_no';
        break;
    }
    switch ($this->order) {
      case 'ascending':
        $string_order = 'ASC';
        break;
      case 'descending':
        $string_order = 'DESC';
        break;
    }
    $this->query .= <<<EOT
    ORDER BY $string_sort $string_order\n
    EOT;
  }

}
