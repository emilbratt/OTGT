<?php

require_once '../applications/QueryRetail.php';

class APIQueryRetail extends QueryRetail {

  function __construct () {
    parent::__construct();
  }

  public function get_article_id ($barcode) {
    $this->query .= <<<EOT
    SELECT
      Article.articleId AS articleid
    FROM
      Article
    INNER JOIN
      ArticleEAN ON Article.articleId = ArticleEAN.articleId
    WHERE
      ArticleEAN.eanCode = '$barcode'\n
    EOT;
  }

  public function movement ($article_id) {
    $this->query .= <<<EOT
    SELECT stockAdjustmenId, movement, qty, date FROM
    (
      SELECT
        stockAdjustmenId AS stockAdjustmenId,
        adjustmentQty AS qty,
        adjustmentDate AS date,
        CASE
          WHEN adjustmentCode = '1' THEN 'korreksjon minus'
          WHEN adjustmentCode = '2' THEN 'korreksjon pluss'
          WHEN adjustmentCode = '3' THEN 'telling'
          WHEN adjustmentCode = '4' THEN 'mottak fra bestilling'
          WHEN adjustmentCode = '9' THEN 'salg' -- NOTE: N < 0 = removed from sales header "fjernet fra bong"
          WHEN adjustmentCode = '10' THEN 'kreditering'
          WHEN adjustmentCode = '33' THEN 'tilleggende telling'
          WHEN adjustmentCode = '41' THEN 'varemottak'
          WHEN adjustmentCode = '91' THEN 'intern pakkeseddel el. web-pakkeseddel'
        END AS movement
      FROM
        StockAdjustment
      WHERE
        articleId = '$article_id'
    ) a
    ORDER BY
     date DESC\n
    EOT;
  }

  public function sales_count ($article_id, $adjustment_id = '0') {
    // if $adjustment_id = 0 it will include all records
    $this->query .= <<<EOT
    SELECT SUM(sales_qty - credit_qty) AS sales_count FROM
    (
      SELECT
        -- mother query takes these summarizes these values, but
        -- the nested queries might return a null value if no rows returned
        -- so we force the null value to become 0 to make aggregation possible
        CASE
          WHEN sales_qty = NULL THEN '0' ELSE sales_qty
        END AS sales_qty,
        CASE
          WHEN credit_qty = NULL THEN '0' ELSE credit_qty
        END AS credit_qty
      FROM
      (
      SELECT
          SUM(adjustmentQty) as sales_qty
      FROM
          StockAdjustment
      WHERE
          articleId = '$article_id'
          AND stockAdjustmenId >= '$adjustment_id'
          AND adjustmentCode  = '9'
      )sales,
      (
      SELECT
          SUM(adjustmentQty) as credit_qty
      FROM
          StockAdjustment
      WHERE
          articleId = '$article_id'
          AND stockAdjustmenId >= '$adjustment_id'
          AND adjustmentCode  = '10'
      )credit
    )summary_table

    EOT;
  }

  public function min_stock_adjustment_id_for_day_back ($days_back = 0) {
    $this->query .= <<<EOT
    SELECT TOP 1
      stockAdjustmenId AS stock_adjustment_id
    FROM
      StockAdjustment
    WHERE
      CONVERT(VARCHAR(10), [adjustmentDate], 102) >= CONVERT(VARCHAR(10), DATEADD(DAY, -$days_back, CURRENT_TIMESTAMP), 102)
      -- adjustmentDate >= DATEADD(DD, -$days_back, CURRENT_TIMESTAMP)
    ORDER BY
      stockAdjustmenId asc
    EOT;
  }
}
