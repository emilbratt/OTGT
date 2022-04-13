<?php

class QueryDatawarehouse {

    protected $query;
    protected $illegal_reserved_words;

    function __construct () {
      $this->illegal_reserved_words = [
        'DATABASE', 'DELETE', 'MODIFY', 'UPDATE', 'INSERT', 'DROP',
      ];
    }

    private function start_new () {
      $this->query = '';
    }

    public function insert_placement () {
      $this->query = <<<EOT
      INSERT INTO `placement`
          (article_id, stock_location, timestamp, yyyymmdd)
      VALUES
          (:article_id, :shelf, :timestamp, :yyyymmdd);
      EOT;
    }

    public function get () {
      $query = $this->query;
      $this->start_new();
      return $query;
    }
}
