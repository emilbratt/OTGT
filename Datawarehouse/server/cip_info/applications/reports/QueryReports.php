<?php

require_once '../applications/QueryRetail.php';

class QueryReports extends QueryRetail {

  protected $time_span;
  protected $date_part;
  protected $items;
  protected $sort;
  protected $order;
  private $where_clause_datestring;

  function __construct () {
    parent::__construct();

    $this->time_span = 'thisday';
    if(isset($_GET['date_type'])) {
      $this->time_span = $_GET['date_type'];
    }

    $this->items = 'all';
    if(isset($_GET['items'])) {
      $this->items = $_GET['items'];
    }

    $this->order = 'ascending';
    if(isset($_GET['order'])) {
      $this->order = $_GET['order'];
    }
  }

  private function add_where_clause_date ($field_name) {
    switch ($this->time_span) {
      case 'thisday':
        $this->query .= <<<EOT
          AND CONVERT(VARCHAR(10), $field_name, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)\n
        EOT;
        break;
      case 'thisweek':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, $field_name) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(WEEK, $field_name) = DATEPART(WEEK, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'thismonth':
        $this->query .= <<<EOT
          AND DATEPART(YEAR, $field_name) = DATEPART(YEAR, CURRENT_TIMESTAMP)
          AND DATEPART(MONTH, $field_name) = DATEPART(MONTH, CURRENT_TIMESTAMP)\n
        EOT;
        break;
      case 'calendar':
        $calendar_from_date = str_replace('-', '.', $_GET['calendar_from_date']);
        $calendar_to_date = str_replace('-', '.', $_GET['calendar_to_date']);
        $this->query .= <<<EOT
          AND CONVERT(VARCHAR(10), $field_name, 102)
            BETWEEN '$calendar_from_date'
            AND '$calendar_to_date'\n
        EOT;
        break;
      default:
        $this->query .= <<<EOT
          AND CONVERT(VARCHAR(10), $field_name, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)\n
        EOT;
    }
  }

  private function add_where_clause_article_status () {
    $this->article_status = 'all';
    if(isset($_GET['article_status'])) {
      $this->article_status = $_GET['article_status'];
    }
    switch ($this->article_status) {
      case 'all':
        break;
      case 'expired':
        $this->query .= <<<EOT
          AND Article.articleStatus = '9'\n
        EOT;

        // not used now: this select article status based on article name
        // $this->query .= <<<EOT
        //   AND Article.articleName LIKE '[.]%'\n
        // EOT;
        break;
      case 'active':
        $this->query .= <<<EOT
          AND Article.articleStatus = '0'\n
        EOT;

        // not used now: this select article status based on article name
        // $this->query .= <<<EOT
        //   AND Article.articleName NOT LIKE '[.]%'\n
        // EOT;
        break;
    }

  }

  private function add_where_clause_sort () {
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
      case 'stock_quantity':
        $string_sort = 'stock_quantity';
        break;
      case 'lastsold':
        $string_sort = 'articleStock.lastSold';
        break;
      case 'location':
        $string_sort = 'location';
        break;
      case 'paymentmethod':
        $string_sort = 'CustomerSaleHeader.additionalInfo';
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
      case 'salesdate':
        $string_sort = 'CustomerSaleHeader.salesDate';
        break;
      case 'sold_price':
        $string_sort = 'customerSales.usedPricePerUnit';
        break;
      case 'discount':
        $string_sort = 'CustomerSales.disCount';
        break;
      case 'seller_name':
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


  public function sold_out () {
    $_date = 'CONVERT(VARCHAR(10), articleStock.lastSold, 105)';
    if ($this->time_span == 'thisday') {
      $_date = 'CONVERT(VARCHAR(5), articleStock.lastSold, 8)';
    }

    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST (stockQty AS INT) AS stock_quantity,
      articleStock.StorageShelf AS location,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS lastimported,
      $_date AS lastsold,
      Article.suppliers_art_no AS supplyid
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    WHERE
      /* items less than -100 are ignored */
      stockQty BETWEEN '-100' AND '0'\n
    EOT;
    $this->add_where_clause_article_status();
    $this->add_where_clause_date('articleStock.lastSold');
    $this->sort = 'lastsold';
    $this->add_where_clause_sort();
  }

  public function imported () {
    $_date = 'CONVERT(VARCHAR(10), lastReceivedFromSupplier, 105)';
    if ($this->time_span == 'thisday') {
      $_date = 'CONVERT(VARCHAR(5), lastReceivedFromSupplier, 8)';
    }
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST(StockAdjustment.adjustmentQty AS INT) AS import_qty,
      CAST (stockQty AS INT) AS stock_quantity,
      articleStock.StorageShelf AS location,
      Article.suppliers_art_no AS supplyid,
      $_date AS lastimported
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    INNER JOIN
      StockAdjustment ON Article.articleId = StockAdjustment.articleId\n
    EOT;

    // START SUB QUERY
    $this->query .= <<<EOT
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
    $this->add_where_clause_article_status();
    $this->add_where_clause_date('[adjustmentDate]');
    // END SUB QUERY
    $this->query .= ")\n";

    $this->sort = 'lastimported';
    $this->add_where_clause_sort();
  }

  public function sales_history () {
    $_date = 'CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 105)';
    if ($this->time_span == 'thisday') {
      $_date = 'CONVERT(VARCHAR(5), CustomerSaleHeader.salesDate, 8)';
    }

    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      hipUser.userFirstName AS seller_name,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST(CustomerSales.noOfArticles AS INT) AS soldqty,
      $_date AS salesdate,
      CustomerSales.usedPricePerUnit AS sold_price,
      CustomerSales.disCount AS discount,
      CustomerSaleHeader.additionalInfo AS paymentmethod,
      Article.suppliers_art_no AS supplyid,
      articleStock.StorageShelf AS location
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
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    WHERE
      Article.articleId IS NOT NULL\n
    EOT;
    $this->add_where_clause_date('CustomerSaleHeader.salesDate');
    $this->add_where_clause_article_status();
    $this->sort = 'salesdate';
    $this->add_where_clause_sort();

  }

  public function in_stock_not_sold_lately () {
    $brand = $_GET['input_field_brand'];
    $location = $_GET['input_field_location'];
    $num_year = $_GET['input_field_date_part_num'];
    $stock_operator = $_GET['input_field_stock_operator'];
    $date_part_type = $_GET['input_field_date_part_type'];
    $stock_limit = $_GET['input_field_stock_num'];
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CONVERT(VARCHAR(10), articleStock.lastSold, 23) AS lastsold,
      CAST (articleStock.stockQty AS INT) AS stock_quantity,
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
      articleStock.stockQty $stock_operator '$stock_limit'
      AND articleStock.lastSold < DATEADD($date_part_type, -$num_year, CURRENT_TIMESTAMP)\n
    EOT;
    if ($location !== '') {
      $this->query .= <<<EOT
        AND articleStock.StorageShelf LIKE '$location%'\n
      EOT;
    }
    if ($brand !== '') {
      $this->query .= <<<EOT
        AND Brands.brandLabel LIKE '%$brand%'\n
      EOT;
    }
    $this->sort = 'lastsold';
    $this->add_where_clause_sort();
  }

  public function sales_per_hour () {
    $year = $_GET['input_field_YYYY'];
    $month = $_GET['input_field_MM'];
    $dom = $_GET['input_field_DOM'];
    $dow = $_GET['input_field_DOW'];
    $hod = $_GET['input_field_HOD'];
    $where_condition = "YEAR(CustomerSaleHeader.salesDate) = $year\n";

    if ( !(empty($month)) ) {
      $where_condition .= "  AND MONTH(CustomerSaleHeader.salesDate) = $month\n";
    }
    if ( !(empty($dom)) ) {
      $where_condition .= "  AND DAY(CustomerSaleHeader.salesDate) = $dom\n";
    }
    if ( !(empty($dow)) ) {
      $where_condition .= "  AND DATEPART(WEEKDAY, CustomerSaleHeader.salesDate) = $dow\n";
    }
    if ( !(empty($hod)) ) {
      $where_condition .= "  AND DATEPART(HOUR, CustomerSaleHeader.salesDate) = $hod\n";
    }

    $this->query .= <<<EOT
    SELECT
      DATEPART(HOUR, CustomerSaleHeader.salesDate) AS at_hour,
      COUNT(CustomerSaleHeader.customerSaleHeaderId) AS total_sales,
      CEILING(SUM(CustomerSaleHeader.netpayed)) AS total_net_sum,
      CEILING(SUM(CustomerSaleHeader.totalPayed)) AS total_sum
    FROM
      CustomerSaleHeader
    WHERE
      $where_condition
    GROUP BY
      DATEPART(hour, CustomerSaleHeader.salesDate)\n
    EOT;

    $this->sort = 'at_hour';
    if(isset($_GET['sort'])) {
      $this->sort = $_GET['sort'];
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
    ORDER BY
      $this->sort $string_order\n
    EOT;
  }

}
