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
            BETWEEN
              '$calendar_from_date'
            AND
              '$calendar_to_date'\n
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

  private function add_order_by_sort () {
    if(isset($_GET['sort'])) {
      $this->sort = $_GET['sort'];
    }
    switch ($this->sort) {
      case 'article':
        $string_sort = 'Article.articleName';
        break;
      case 'Article.articleName':
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
        $string_sort = 'articleStock.StorageShelf';
        break;
      case 'paymentmethod':
        $string_sort = 'CustomerSaleHeader.additionalInfo';
        break;
      case 'importquantity':
        $string_sort = 'StockAdjustment.adjustmentQty';
        break;
      case 'lastimported':
        $string_sort = 'articleStock.lastReceivedFromSupplier';
        break;
      case 'supplyid':
        $string_sort = 'Article.suppliers_art_no';
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
      case 'abc_code':
        $string_sort = 'abc_code';
        break;
      case 'sales_total':
        $string_sort = 'sales_total';
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
    $this->add_order_by_sort();
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
    $this->add_order_by_sort();
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
    $this->add_order_by_sort();

  }

  public function in_stock_not_sold_lately () {
    $brand = $_GET['input_field_brand'];
    $brand = str_replace("'", '_', $brand);
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
    $this->add_order_by_sort();
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

  public function all_brands () {
    $this->query .= <<<EOT
    SELECT
      brandId AS brand_id,
      brandLabel AS brand
    FROM
      Brands
    WHERE
      brandLabel IS NOT NULL
      AND DATALENGTH(brandLabel) > 0
    ORDER BY
      brandLabel
    EOT;
  }

  public function brand_by_brand_id ($brand_id = false) {
    if ( isset($_GET['brand_id']) ) {
      $brand_id = $_GET['brand_id'];
    }
    if ($brand_id === false) {
      return false;
    }
    if ( is_numeric($brand_id) ) {
      $this->query .= <<<EOT
      SELECT brandLabel AS brand
      FROM   Brands
      WHERE  brandId = '$brand_id'
      EOT;
    }
  }

  public function brand_full_overview ($brand_id = false) {
    if ($brand_id === false) {
      return false;
    }
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS article_id,
      Brands.brandLabel AS brand_name,
      Article.articleName AS article_name,
      Article.abc_code AS abc_code, -- abc codes e.g. computing velocity codes to measure sales performance
      CAST (articleStock.stockQty AS INT) AS stock_quantity,

      movement_summary.sum_manual_adjust AS manual_adjustment_total,
      CONVERT(VARCHAR(10), movement_summary.min_man_minus_date, 23) AS min_man_minus_date,
      CONVERT(VARCHAR(10), movement_summary.max_man_minus_date, 23) AS max_man_minus_date,
      CONVERT(VARCHAR(10), movement_summary.min_man_plus_date, 23) AS min_man_plus_date,
      CONVERT(VARCHAR(10), movement_summary.max_man_plus_date, 23) AS max_man_plus_date,

      movement_summary.sum_sales AS sales_total,
      CONVERT(VARCHAR(10), articleStock.lastSold, 23) AS lastsold,
      CONVERT(VARCHAR(10), movement_summary.min_sales_date, 23) AS min_sales_date,
      CONVERT(VARCHAR(10), movement_summary.max_sales_date, 23) AS max_sales_date,
      CONVERT(VARCHAR(10), movement_summary.min_credit_date, 23) AS min_credit_date,
      CONVERT(VARCHAR(10), movement_summary.max_credit_date, 23) AS max_credit_date,

      movement_summary.receive_qty AS received_total,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 23) AS lastimported,
      CONVERT(VARCHAR(10), movement_summary.min_receive_date, 23) AS min_receive_date,
      CONVERT(VARCHAR(10), movement_summary.max_receive_date, 23) AS max_receive_date,

      Article.suppliers_art_no AS supplyid

    FROM
      Article
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
    (

      SELECT
        Article.articleId AS mov_article_id,
        mov_qty_sum.min_man_minus_date,
        mov_qty_sum.max_man_minus_date,

        mov_qty_sum.min_man_plus_date,
        mov_qty_sum.max_man_plus_date,

        mov_qty_sum.min_sales_date,
        mov_qty_sum.max_sales_date,

        mov_qty_sum.min_credit_date,
        mov_qty_sum.max_credit_date,

        mov_qty_sum.min_receive_date,
        mov_qty_sum.max_receive_date,

        SUM(mov_qty_sum.man_plus_qty - mov_qty_sum.man_minus_qty) AS sum_manual_adjust,
        SUM(mov_qty_sum.sales_qty - mov_qty_sum.credit_qty) AS sum_sales,
        mov_qty_sum.receive_qty
      FROM
        Article
      INNER JOIN
      (
        SELECT
          Article.articleId AS mov_sum_article_id,
          CASE
            WHEN man_minus_qty IS NULL THEN '0'
            ELSE man_minus_qty
          END AS man_minus_qty,
          min_man_minus_date,
          max_man_minus_date,

          CASE
            WHEN man_plus_qty IS NULL THEN '0'
            ELSE man_plus_qty
          END AS man_plus_qty,
          min_man_plus_date,
          max_man_plus_date,

          CASE
            WHEN sales_qty IS NULL THEN '0'
            ELSE sales_qty
          END AS sales_qty,
          min_sales_date,
          max_sales_date,

          CASE
            WHEN credit_qty IS NULL THEN '0'
            ELSE credit_qty
          END AS credit_qty,
          min_credit_date,
          max_credit_date,

          CASE
            WHEN receive_qty IS NULL THEN '0'
            ELSE receive_qty
          END AS receive_qty,
          min_receive_date,
          max_receive_date

        FROM
          Article
        LEFT JOIN
        (

          SELECT
            Article.articleId AS code_1_article_id,
            CAST(SUM(adjustmentQty) AS INT) AS man_minus_qty,
            MIN(StockAdjustment.adjustmentDate) AS min_man_minus_date,
            MAX(StockAdjustment.adjustmentDate) AS max_man_minus_date
          FROM
            StockAdjustment
          INNER JOIN
            Article ON StockAdjustment.articleId = Article.articleId
          INNER JOIN
            Brands ON Article.brandId = Brands.brandId

          WHERE
            StockAdjustment.adjustmentCode  = '1' -- code for manual correction minus
            AND Brands.brandId = '$brand_id'


    EOT;
    $this->add_where_clause_date('StockAdjustment.adjustmentDate');
    $this->query .= <<<EOT

          GROUP BY
            Article.articleId

        )code_1 ON Article.articleId = code_1.code_1_article_id
        LEFT JOIN

        (
          SELECT
            Article.articleId AS code_2_article_id,
            CAST(SUM(adjustmentQty) AS INT) AS man_plus_qty,
            MIN(StockAdjustment.adjustmentDate) AS min_man_plus_date,
            MAX(StockAdjustment.adjustmentDate) AS max_man_plus_date
          FROM
            StockAdjustment
          INNER JOIN
            Article ON StockAdjustment.articleId = Article.articleId
          INNER JOIN
            Brands ON Article.brandId = Brands.brandId

          WHERE
            StockAdjustment.adjustmentCode  = '2' -- code for manual correction plus
            AND Brands.brandId = '$brand_id'

    EOT;
    $this->add_where_clause_date('StockAdjustment.adjustmentDate');
    $this->query .= <<<EOT

          GROUP BY
            Article.articleId

        )code_2 ON Article.articleId = code_2.code_2_article_id

        LEFT JOIN
        (

          SELECT
            Article.articleId AS code_9_article_id,
            CAST(SUM(adjustmentQty) AS INT) AS sales_qty,
            MIN(StockAdjustment.adjustmentDate) AS min_sales_date,
            MAX(StockAdjustment.adjustmentDate) AS max_sales_date
          FROM
            StockAdjustment
          INNER JOIN
            Article ON StockAdjustment.articleId = Article.articleId
          INNER JOIN
            Brands ON Article.brandId = Brands.brandId

          WHERE
            StockAdjustment.adjustmentCode  = '9' -- code for sales
            AND Brands.brandId = '$brand_id'

    EOT;
    $this->add_where_clause_date('StockAdjustment.adjustmentDate');
    $this->query .= <<<EOT

          GROUP BY
            Article.articleId

        )code_9 ON Article.articleId = code_9.code_9_article_id
        LEFT JOIN

        (
          SELECT
            Article.articleId AS code_10_article_id,
            CAST(SUM(adjustmentQty) AS INT) AS credit_qty,
            MIN(StockAdjustment.adjustmentDate) AS min_credit_date,
            MAX(StockAdjustment.adjustmentDate) AS max_credit_date
          FROM
            StockAdjustment
          INNER JOIN
            Article ON StockAdjustment.articleId = Article.articleId
          INNER JOIN
            Brands ON Article.brandId = Brands.brandId

          WHERE
            StockAdjustment.adjustmentCode  = '10' -- code for credit
            AND Brands.brandId = '$brand_id'

    EOT;
    $this->add_where_clause_date('StockAdjustment.adjustmentDate');
    $this->query .= <<<EOT

          GROUP BY
            Article.articleId

        )code_10 ON Article.articleId = code_10.code_10_article_id

        LEFT JOIN
        (
          SELECT
            Article.articleId AS code_41_article_id,
            CAST(SUM(adjustmentQty) AS INT) AS receive_qty,
            MIN(StockAdjustment.adjustmentDate) AS min_receive_date,
            MAX(StockAdjustment.adjustmentDate) AS max_receive_date
          FROM
            StockAdjustment
          INNER JOIN
            Article ON StockAdjustment.articleId = Article.articleId
          INNER JOIN
            Brands ON Article.brandId = Brands.brandId

          WHERE
            StockAdjustment.adjustmentCode  = '41' -- code for credit
            AND Brands.brandId = '$brand_id'

    EOT;
    $this->add_where_clause_date('StockAdjustment.adjustmentDate');
    $this->query .= <<<EOT

          GROUP BY
            Article.articleId

        )code_41 ON Article.articleId = code_41.code_41_article_id

        WHERE
          Article.articleId = code_9.code_9_article_id
          OR Article.articleId  = code_10.code_10_article_id
          OR Article.articleId  = code_41.code_41_article_id

      )mov_qty_sum ON Article.articleId = mov_qty_sum.mov_sum_article_id
      GROUP BY
        mov_qty_sum.receive_qty,
        mov_qty_sum.min_man_minus_date,
        mov_qty_sum.max_man_minus_date,
        mov_qty_sum.min_man_plus_date,
        mov_qty_sum.max_man_plus_date,
        mov_qty_sum.min_sales_date,
        mov_qty_sum.max_sales_date,
        mov_qty_sum.min_credit_date,
        mov_qty_sum.max_credit_date,
        mov_qty_sum.min_receive_date,
        mov_qty_sum.max_receive_date,
        Article.articleId

    )movement_summary ON Article.articleId = movement_summary.mov_article_id
    WHERE Article.articleId IS NOT NULL\n
    EOT;
    $this->add_where_clause_article_status();
    $this->sort = 'Article.articleName';
    $this->add_order_by_sort();
    if ($this->sort !== 'Article.articleName') {
      $this->query .= ',Article.articleName';
    }
  }

}
