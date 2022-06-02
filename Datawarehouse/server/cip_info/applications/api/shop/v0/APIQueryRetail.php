<?php

require_once '../applications/QueryRetail.php';

class APIQueryRetail extends QueryRetail {

  function __construct () {
    parent::__construct();
  }

  public function howbusy ($minutes = '5', $min_customer_sales_id_today = false) {
    // seed in minutes = how many minutes back when including sales
    // default is all sales last "5" minutes
    $where_condition = "CustomerSaleHeader.salesDate > DATEADD(mi, -$minutes, CURRENT_TIMESTAMP)\n";
    if ($min_customer_sales_id_today !== false) {
      // passing min_customer_sales_id_today helps speed up the query
      $where_condition .= "  AND CustomerSalesId >= '$min_customer_sales_id_today'";
    }
    $this->query .= <<<EOT
    SELECT
      SUM(total_sales) AS sales,
      COUNT(user_id) AS sellers,
      CASE
        WHEN SUM(total_sales) / COUNT(user_id) IS NULL THEN 0
        WHEN SUM(total_sales) / COUNT(user_id) > 10 THEN 10
        WHEN SUM(total_sales) / COUNT(user_id) < 0 THEN 0
        ELSE SUM(total_sales) / COUNT(user_id)
      END AS busy_result
    FROM
    (
      SELECT
        CustomerSaleHeader.userId AS user_id,
        COUNT(CustomerSales.CustomerSalesId) AS total_sales
      FROM
        CustomerSaleHeader
      INNER JOIN
        CustomerSales
      ON
        CustomerSaleHeader.customerSaleHeaderId = CustomerSales.customerSaleHeaderId
      WHERE
        $where_condition
      GROUP BY
        CustomerSaleHeader.userId
    ) inner_table
    EOT;
  }

}
