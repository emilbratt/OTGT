<?php

class Developing {

  protected $page = 'Utvikling';
  protected $environment;
  protected $template;
  protected $database;
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
    $this->navigation = new NavigationDeveloping();
    $this->template = new TemplateDeveloping();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

  protected function run_sql_shell_query () {
    // for the SQL shells
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


class Home extends Developing {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->print();
  }

}


class SQLShellRetail extends Developing {

  public function run () {
    $this->database = new DatabaseRetail();
    $this->query = 'SELECT TOP 3 articleId AS Vareid, articleName AS Varenavn FROM Article';
    if(isset($_POST['sql_shell_query'])) {
      $this->query = $_POST['sql_shell_query'];
    }

    $this->template->sql_shell_form($this->query);
    if(isset($_POST['sql_shell_query'])) {
      $this->run_sql_shell_query();
    }

    $this->template->print();
  }

}


class SQLShellDatawarehouse extends Developing {

  public function run () {
    $this->database = new DatabaseDatawarehouse();
    $this->query = 'SELECT article_id AS Vareid, art_name AS Varenavn FROM articles LIMIT 3';
    if(isset($_POST['sql_shell_query'])) {
      $this->query = $_POST['sql_shell_query'];
    }

    $this->template->sql_shell_form($this->query);
    if(isset($_POST['sql_shell_query'])) {
      $this->run_sql_shell_query();
    }

    $this->template->print();
  }

}


class FetchAPI extends Developing {

  public function run () {
    $this->template->title('testing requests using fetch api');
    $this->template->message('about: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API');
    $link = new Hyperlink();
    $link->link_redirect('api');
    $api_home = $link->url;
    $this->template->message($api_home);
    // since api is called from our browser -> use main host and external port
    $host = $this->environment->datawarehouse('datawarehouse_ip');
    $port = $this->environment->datawarehouse('barcode_generator_external_port');
    // dummy query
    $query = 'shelf/A-A-1';
    $url = 'http://'.$host.':'.$port.'/'.$query;
    $this->template->message($url);
    $script = <<<EOT
    <script>
    const image_url = "$url";

    (async () => {
      const response = await fetch(image_url)
      const image_byte_array = await response.blob()
      const reader = new FileReader();
      reader.readAsDataURL(image_byte_array);
      reader.onloadend = () => {
        const base64data = reader.result;
        console.log(base64data);
      }
    })()

    window.open(image_url,'Image');
    </script>
    EOT;
    $link = null;

    $this->template->custom_script($script);
    $this->template->print();
  }

}


class Testing extends Developing {

  public function run () {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_internal_port');
    $query = 'shelf/A-A-1';
    $url = 'http://'.$host.':'.$port.'/'.$query;
    header("Content-Type: image/png");
    $curl = curl_init();
    curl_setopt( $curl, CURLOPT_URL, $url );
    $body = curl_exec( $curl );
    curl_close( $curl );
    echo $body;
  }

}
