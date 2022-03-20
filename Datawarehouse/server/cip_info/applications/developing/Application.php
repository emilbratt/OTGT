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
    require_once '../applications/HyperLink.php';
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


class FetchAPI extends Developing {

  public function run () {
    // fetch json content from api application
    // api application not ready
    $this->template->title('testing requests using fetch api');
    $this->template->message('about: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API');
    $link = new Hyperlink();
    $link->link_redirect('api');
    $api_home = $link->url;
    $this->template->message($api_home);
    $script = <<<EOT
    <script>
    console.log('Hello World');
    console.log(fetch('$api_home'))
      <!-- then(res => console.log(res)) -->
    </script>
    EOT;
    $link = null;
    $this->template->custom_script($script);
    $this->template->print();
  }

}


class Testing extends Developing {

  public function run () {
    $this->template->message('testing stuff');
    $this->template->print();
  }

}
