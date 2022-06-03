<?php

require_once '../applications/QueryRetail.php';

class APIQueryRetail extends QueryRetail {

  function __construct () {
    parent::__construct();
  }

  public function salesperhour ($year = false, $month = 0, $day = 0) {
    if ($year === false ) {
      return false;
    }
    $where_condition = "YEAR(CustomerSaleHeader.salesDate) = $year\n";
    if ($month !== 0) {
      $where_condition .= "  AND MONTH(CustomerSaleHeader.salesDate) = $month\n";
    }
    if ($day !== 0) {
      $where_condition .= "  AND DAY(CustomerSaleHeader.salesDate) = $day\n";
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
      DATEPART(hour, CustomerSaleHeader.salesDate)
    ORDER BY
      total_net_sum DESC
    EOT;
  }

}
