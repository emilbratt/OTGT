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

  public function update_timestamp_for_placement () {
    $this->query = <<<EOT
    UPDATE placement
    SET timestamp = :timestamp, yyyymmdd = :yyyymmdd
    WHERE article_id = :article_id AND stock_location = :shelf
    EOT;
  }

    public function get () {
      $query = $this->query;
      $this->start_new();
      return $query;
    }
}
