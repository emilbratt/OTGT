<?php

require_once '../applications/QueryDatawarehouse.php';

class QueryDatawarehouseHome extends QueryDatawarehouse {

  function __construct () {
    parent::__construct();
  }

  public function remove_note_from_yesterday () {
    // any note from yesterday or earlier will be deleted
    $this->query .= <<<EOT
    DELETE FROM cip_cache
    WHERE
      mem_key = 'home_page_note'
      AND DATE(mem_time) < DATE(CURDATE())\n
    EOT;
  }

}
