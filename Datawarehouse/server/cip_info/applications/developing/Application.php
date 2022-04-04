<?php

class Developing {

  protected $page = 'Devtools';
  protected $environment;
  protected $template;
  protected $database;
  protected $db_host;
  protected $db_name;
  protected $stmt;
  protected $col_count;
  protected $row_count;
  protected $utf_convert = false;
  protected $navigation;
  protected $query;
  protected $fields;
  protected $result;

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/developing/TemplateDeveloping.php';
    require_once '../applications/developing/NavigationDeveloping.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationDeveloping();
    $this->template = new TemplateDeveloping();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

  protected function load_sql_shell () {
    if(isset($_POST['sql_shell_query'])) {
      $this->query = $_POST['sql_shell_query'];
    } else {
      // if no query is passed, we assume first visit and therefore show db info
      $this->template->title('Host: ' . $this->db_host,'Database: ' . $this->db_name);
      $this->template->title('Database: ' . $this->db_name);
    }

    $this->template->sql_shell_form($this->query);
    if(isset($_POST['sql_shell_query'])) {
      $this->run_sql_shell_query();
    }
  }

  protected function run_sql_shell_query () {
    // for the SQL shells
    $this->stmt = $this->database->cnxn->prepare($this->query);
    $this->stmt->execute();
    $this->col_count = $this->stmt->columnCount();
    if ($this->col_count <= 0) {
      return;
    }
    $this->result = $this->stmt->fetchAll();
    // unlike PDOStatement::columnCount, PDOStatement::rowCount(); is not stable
    // across all drivers, so we simply pass the array to php's count() instead
    $this->row_count = count($this->result);
    // if our database has no unicode, we need to handle language specific
    // symbols like Æ,Ø and Å correctly by converting UTF-8 to ISO-XXXX

    $this->template->table_full_width_start();
    $this->template->table_row_start();
    for ($i = 0; $i <= $this->col_count; $i++) {
      $col = $this->stmt->getColumnMeta($i);
      if(isset($col['name'])) {
        switch ($this->utf_convert) {
          case true;
            $this->template->table_row_header(CharacterConvert::utf_to_norwegian($col['name']));
            break;
          case false;
            $this->template->table_row_header($col['name']);
            break;
        }
      }
    }
    $this->template->table_row_end();
    for ($i = 0; $i < $this->row_count; $i++) {
      $row = $this->result[$i];
      $this->template->table_row_start();
      for ($j = 0; $j < $this->col_count; $j++) {
        switch ($this->utf_convert) {
          case true;
            $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row[$j]));
            break;
          case false;
            $this->template->table_row_value($row[$j]);
            break;
        }
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
    $this->db_host = $this->environment->retail('db_host');
    $this->db_name = $this->environment->retail('db_name');
    $this->utf_convert = true;
    $this->database = new DatabaseRetail();
    $this->query = 'SELECT TOP 3 articleId, articleName FROM Article';
    $this->load_sql_shell();
    $this->template->print();
  }

}


class SQLShellDatawarehouse extends Developing {

  public function run () {
    $this->db_host = $this->environment->datawarehouse('db_host');
    $this->db_name = $this->environment->datawarehouse('db_name');
    $this->utf_convert = false;
    $this->database = new DatabaseDatawarehouse();
    $this->query = 'SELECT article_id, art_name FROM articles LIMIT 3';
    $this->load_sql_shell();
    $this->template->print();
  }

}


class FetchAPI extends Developing {

  public function run () {
    $this->template->title('testing requests using fetch api');
    $this->template->message('about: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API');
    $hyperlink = new Hyperlink();
    $hyperlink->link_redirect('api');
    $api_home = $hyperlink->url;
    $this->template->message($api_home);
    // since api is called from our browser -> use main host and external port
    $host = $this->environment->datawarehouse('datawarehouse_ip');
    $port = $this->environment->datawarehouse('barcode_generator_external_port');
    $endpoint = 'shelf/';
    $query = 'A-A-1';
    $url = 'http://' . $host . ':' . $port . '/' . $endpoint . $query;
    $this->template->message($url);
    $this->template->hyperlink_button("Barcode $query", $url);
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
    </script>
    EOT;

    $link = null;

    $this->template->custom_script($script);
    $this->template->print();
  }

}


class Test extends Developing {

  public function run () {
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_internal_port');
    $endpoint = 'shelf/A-A-1';
    $url = 'http://' . $host . ':' . $port . '/' . $endpoint;
    header("Content-Type: image/png");
    $curl = curl_init();
    curl_setopt( $curl, CURLOPT_URL, $url );
    $body = curl_exec( $curl );
    curl_close( $curl );
    echo $body;
  }

}


class Performance extends Developing {

  private $remainder;
  private $iterations;
  private $start_time;
  private $dummy_var;
  protected $time_total;

  public function run () {
    $hyperlink = new HyperLink();
    $this->iterations = 100000000;

    $this->template->title('If vs Swtich');
    $this->template->message("Number of Iterations: $this->iterations");
    $this->template->message('Expect to wait several seconds for results');
    $hyperlink->add_query('run', 'true');
    $this->template->hyperlink_button('Run test', $hyperlink->url);
    if ( isset($_GET['run']) ) {
      if ($_GET['run'] == 'true') {
        $this->test_if();
        $this->test_switch();
      }
    }
    $this->template->print();
  }

  private function test_if () {
    $this->start_time = time();
    for ($i = 0; $i < $this->iterations; ++$i) {
      $this->remainder = $i%10;
      if ($this->remainder == 1) {
        $this->dummy_function();
      } elseif ($this->remainder == 2) {
        $this->dummy_function();
      } elseif ($this->remainder == 3) {
        $this->dummy_function();
      } elseif ($this->remainder == 4) {
        $this->dummy_function();
      } elseif ($this->remainder == 5) {
        $this->dummy_function();
      } elseif ($this->remainder == 6) {
        $this->dummy_function();
      } elseif ($this->remainder == 7) {
        $this->dummy_function();
      } elseif ($this->remainder == 8) {
        $this->dummy_function();
      } elseif ($this->remainder == 9) {
        $this->dummy_function();
      } else {
        $this->dummy_function();
      }
    }
    $this->time_total = ( round(time()) - round($this->start_time));
    $this->template->message("if statement time in seconds: $this->time_total");
  }

  private function test_switch () {
    $this->start_time = time();
    for ($i = 0; $i < $this->iterations; ++$i) {
      $this->remainder = $i%10;
      switch ($this->remainder) {
      case 1:
        $this->dummy_function();
        break;
      case 2:
        $this->dummy_function();
        break;
      case 3:
        $this->dummy_function();
        break;
      case 4:
        $this->dummy_function();
        break;
      case 5:
        $this->dummy_function();
        break;
      case 6:
        $this->dummy_function();
        break;
      case 7:
        $this->dummy_function();
        break;
      case 8:
        $this->dummy_function();
        break;
      case 9:
        $this->dummy_function();
        break;
      default:
        $this->dummy_function();
      }
    }
    $this->time_total = (time() - $this->start_time);
    $this->template->message("switch statement time in seconds: $this->time_total");
  }

  private function dummy_function () {
    $dummy_var = 'some value';
    return;
  }
}
