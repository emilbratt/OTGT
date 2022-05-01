<?php

require_once '../applications/QueryDatawarehouse.php';

class QueryDatawarehousePlacement extends QueryDatawarehouse {

  function __construct () {
    parent::__construct();
  }

  public function latest_registered_placements () {
    $this->query .= <<<EOT
    SELECT article_id, stock_location, timestamp,
    CASE
      WHEN DATE(timestamp) = DATE(NOW()) THEN DATE_FORMAT(timestamp, '%H:%i')
      ELSE DATE_FORMAT(timestamp, '%d.%m.%Y')
    END AS format_timestamp
    FROM placement
    ORDER BY timestamp DESC
    LIMIT 20\n
    EOT;
  }

}
