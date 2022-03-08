<?php

class Developing {

  protected $page = 'Utvikling'; // alias for top_navbar
  protected $environment;
  protected $template;
  protected $navigation;
  protected $query;
  protected $fields;
  protected $result;


  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/developing/TemplateDeveloping.php';
    require_once '../applications/developing/NavigationDeveloping.php';

    $this->environment = new Environment();
    $this->database = new DatabaseRetail();
    $this->navigation = new NavigationDeveloping();
    $this->template = new TemplateDeveloping();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Developing {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
  }

}


class SQLShell extends Developing {

  public function run () {

    $this->query = 'SELECT TOP 3 articleId AS Vareid, articleName AS Varenavn FROM Article';
    if(isset($_POST['sql_shell_query'])) {
      $this->query = $_POST['sql_shell_query'];
    }

    $this->template->sql_shell_form($this->query);
    if(isset($_POST['sql_shell_query'])) {
      $this->run_query();
    }

    $this->template->print();
  }

  private function run_query () {
    $this->result = $this->database->cnxn->query($this->query)->fetch();
    if ( !($this->result) ) {
      $this->template->message('no rows');
      return;
    }

    $this->fields = array();
    foreach(array_keys($this->result) as $col) {
      if ( !(is_numeric($col)) ) {
        array_push($this->fields, $col);
      }
    }

    $stmt = $this->database->cnxn->prepare($this->query);
    $stmt->execute();
    $this->col_count = $stmt->columnCount();

    if ($this->col_count <= 0) {
      return;
    }

    $this->result = array();
    while ($row = $stmt->fetch()) {
      array_push($this->result, $row);
    }
    $this->template->table_full_width_start();

    $this->template->table_row_start();
    foreach($this->fields as $v) {
      $this->template->table_row_header($v);
    }
    $this->template->table_row_end();

    foreach ($this->result as $row) {
      $this->template->table_row_start();
        foreach($this->fields as $field) {
          $v = $row[$field];
          $this->template->table_row_value(mb_convert_encoding($v, "UTF-8", "ISO-8859-1"));
        }
      $this->template->table_row_end();
    }
  $this->template->table_end();
  }

}


class API extends Developing {

  public function run () {
    $this->template->message('api for testing');
    $this->template->print();
  }

}


class Testing extends Developing {

  public function run () {
    require_once '../applications/placement/QueryPlacement.php';
    $this->template->message('Testing whatever needs testing');
    $query = new QueryPlacement();
    $query->insert_placement_datawarehouse();
    $c = $query->get();

    $database = new DatabaseDatawarehouse();
    $stmt = $database->cnxn->prepare($query->get());
    $timestamp = time();
    $timestamp = '1234567890'; // correct timestamp format according to db: 2022-03-08_12:22:15.39
    $values =  ['article_id' => '64600', 'shelf' => 'O-A-15', 'timestamp' => $timestamp, 'yyyymmdd' => '20220308'];
    $stmt->execute($values);
    // check after update: select * from placement where article_id = 64600
    // remove record: delete from placement where timestamp = '1234567890';
    $this->template->print();
  }

}
