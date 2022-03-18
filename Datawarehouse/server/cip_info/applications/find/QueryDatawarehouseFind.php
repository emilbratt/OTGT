<?php

require_once '../applications/QueryDatawarehouse.php';

class QueryDatawarehouseFind extends QueryDatawarehouse {

  function __construct () {
    parent::__construct();
  }

  public function _select_placements_by_article_id () {
    $this->query = <<<EOT
    SELECT DISTINCT
      stock_location
    FROM
      placement
    WHERE
      article_id = :article_id
    ORDER BY
      timestamp DESC
    LIMIT
      10;
    EOT;
  }

}
