<?php

require_once '../applications/QueryRetail.php';

class QueryRetailHome extends QueryRetail {

  protected $time_span;
  protected $items;
  protected $sort;
  protected $order;

  function __construct () {
    parent::__construct();
  }

  public function get_min_customer_sales_id_today () {
    $this->query .= <<<EOT
    SELECT
      MIN(CustomerSales.CustomerSalesId) AS min_id
    FROM
     CustomerSales
    INNER JOIN
      CustomerSaleHeader
    ON
      CustomerSales.customerSaleHeaderId = CustomerSaleHeader.customerSaleHeaderId
    WHERE
      CustomerSaleHeader.salesDate > CAST(CURRENT_TIMESTAMP AS DATE)\n
    EOT;
  }

  public function most_expensive_item_sold_today ($customer_sales_id) {
    $this->query .= <<<EOT
    SELECT TOP 1
      CustomerSaleHeader.customerSaleHeaderId,
      CustomerSaleHeader.userId AS sales_header_id,
      CONVERT(VARCHAR(5), CustomerSaleHeader.salesDate, 108) AS time,
      hipUser.userFirstName AS salesperson,
      CAST(CustomerSales.noOfArticles AS INT) AS soldqty,
      CustomerSales.work_produsent AS brand,
      CustomerSales.usedPricePerUnit as price,
      CustomerSales.work_articlename AS article,
      CustomerSales.articleId AS article_id
    FROM
      CustomerSaleHeader
    INNER JOIN
      CustomerSales
    ON
      CustomerSaleHeader.customerSaleHeaderId = CustomerSales.customerSaleHeaderId
    INNER JOIN
      hipUser
    ON
      CustomerSaleHeader.userId = hipUser.userId
    WHERE
      CustomerSales.CustomerSalesId >= '$customer_sales_id'
      -- CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)

    ORDER BY
      CustomerSales.totalThisSale DESC\n
    EOT;
  }

  public function last_ten_sold_items ($customer_sales_id) {
    $this->query .= <<<EOT
    SELECT TOP 10
      CustomerSaleHeader.customerSaleHeaderId,
      CustomerSaleHeader.userId,
      CONVERT(VARCHAR(5), CustomerSaleHeader.salesDate, 108) AS time,
      hipUser.userFirstName AS seller,
      CustomerSales.work_produsent AS brand,
      CustomerSales.work_articlename AS article,
      CustomerSales.articleId AS article_id
    FROM
      CustomerSaleHeader

    INNER JOIN
      CustomerSales
    ON
      CustomerSaleHeader.customerSaleHeaderId = CustomerSales.customerSaleHeaderId
    INNER JOIN
      hipUser
    ON
      CustomerSaleHeader.userId = hipUser.userId
    WHERE
      CustomerSales.articleId IS NOT NULL
      AND CustomerSales.CustomerSalesId >= '$customer_sales_id'
      --AND CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)
    ORDER BY
      CustomerSaleHeader.salesDate DESC\n
    EOT;
  }

  public function brands_imported_today () {
    $this->query .= <<<EOT
    SELECT
      Brands.brandLabel AS brand,
      COUNT(Brands.brandLabel) AS articles_imported
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
        /* correct day from this YEAR */
        DATEPART(DAYOFYEAR, [adjustmentDate]) = DATEPART(DAYOFYEAR, CURRENT_TIMESTAMP) AND
        /* correct day from this DAY OF YEAR */
        DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, CURRENT_TIMESTAMP) AND

        adjustmentCode ='41' AND
        Stock_Ad.articleId = Article.articleId AND
        Stock_Ad.stockAdjustmenId = StockAdjustment.stockAdjustmenId AND
        Stock_Ad.adjustmentDate = StockAdjustment.adjustmentDate
    )

    GROUP BY
      Brands.brandLabel
    ORDER BY
      Brands.brandLabel\n
    EOT;
  }

  public function turnover_today ($customer_sales_id) {
    $this->query .= <<<EOT
    SELECT
      CAST(SUM(CustomerSales.totalThisSale) AS INT) AS sum_turnover
    FROM
      CustomerSales
    WHERE
      CustomerSales.CustomerSalesId >= '$customer_sales_id'
      AND isGiftCardSaleType = NULL
    \n
    EOT;
  }

  public function turnover_week_behind ($i = 0) {
    $this->query .= <<<EOT
    SELECT
      CASE
        WHEN CAST(SUM(Brto_Salg_Kr) AS INT) IS NULL THEN 0
        ELSE CAST(SUM(Brto_Salg_Kr) AS INT)
      END AS sum_turnover
    FROM
      view_HIP_salesInfo_10
    WHERE
      CONVERT(VARCHAR(10), [salesdate], 102) = CONVERT(VARCHAR(10), DATEADD(WEEK, -$i, CURRENT_TIMESTAMP), 102)
      AND isGiftCard ='0'\n
    EOT;
  }

  public function users_sales_metrics ($customer_sales_id) {
    $this->query .= <<<EOT
    SELECT
      hipUser.userFirstName AS salesperson,
      SUM(CustomerSales.noOfArticles) AS article_count,
      CAST(SUM(CustomerSales.totalThisSale) AS INT) AS total
    FROM
      CustomerSales
    FULL JOIN CustomerSaleHeader
      ON CustomerSales.customerSaleHeaderId = CustomerSaleHeader.customerSaleHeaderId
    FULL JOIN hipUser
      ON CustomerSaleHeader.userId = hipUser.userId
    WHERE
      CustomerSales.CustomerSalesId >= '$customer_sales_id'
      AND isGiftCardSaleType = NULL
    GROUP BY
      hipUser.userFirstName
    ORDER BY
      salesperson ASC\n
    EOT;
  }

}
