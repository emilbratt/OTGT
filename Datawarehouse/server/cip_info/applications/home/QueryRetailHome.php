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

  public function most_expensive_item_sold_today () {
    $this->query .= <<<EOT
    SELECT TOP 1
      CustomerSaleHeader.customerSaleHeaderId,
      CustomerSaleHeader.userId,
      CustomerSaleHeader.totalPayed AS price,
      CONVERT(VARCHAR(5), CustomerSaleHeader.salesDate, 108) AS time,
      hipUser.userFirstName AS salesperson,
      CustomerSales.totalThisSale AS price,
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
      CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)

    ORDER BY
      CustomerSales.totalThisSale DESC\n
    EOT;
  }

  public function last_ten_sold_items () {
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
      AND CONVERT(VARCHAR(10), CustomerSaleHeader.salesDate, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)
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

  public function user_who_sold_most_today () {
    $this->query .= <<<EOT
    SELECT TOP 1
      salesperson,
      article_count
    FROM
      (
        SELECT
        BrukerFornavn AS salesperson,
        SUM(AntallArtikler) AS article_count
      FROM
        view_HIP_SalesInfo_Detail
      WHERE
        CONVERT(VARCHAR(10), SalgsDato, 102) = CONVERT(VARCHAR(10), CURRENT_TIMESTAMP, 102)
        AND BrukerFornavn != ''
      GROUP BY
        BrukerFornavn
      ) sold_most
    ORDER BY
      article_count DESC\n
    EOT;
  }

}
