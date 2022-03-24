<?php

require_once '../applications/QueryRetail.php';

class APIQueryRetail extends QueryRetail {

  function __construct () {
    parent::__construct();
  }


  public function article_movement ($article_id) {
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
          WHEN adjustmentCode = '9' THEN 'salg'
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

}
