<?php

class Developing {

  protected $page = 'Devtools';
  protected $environment;
  protected $navigation;
  protected $template;
  protected $db_host;
  protected $db_name;
  protected $database;
  protected $stmt;
  protected $field_count;
  protected $fields;
  protected $row_count;
  protected $query;
  protected $utf_convert;
  protected $result;

  function __construct () {
    require_once '../applications/DatabaseRetail.php';
    require_once '../applications/DatabaseDatawarehouse.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/HyperLink.php';
    require_once '../applications/developing/TemplateDeveloping.php';
    require_once '../applications/developing/NavigationDeveloping.php';

    // if our database has language specific strings are stored in ASCII,
    // we might need to handle the query results if we want to present these
    // characters correctly by converting the query result to UTF-8 ISO-XXXX
    // ..we set false as default
    $this->utf_convert = false;

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
    $this->stmt = $this->database->cnxn->prepare($this->query);
    $this->stmt->execute();
    $this->field_count = $this->stmt->columnCount();
    $this->result = $this->stmt->fetchAll(PDO::FETCH_ASSOC);
    // unlike PDOStatement::columnCount, PDOStatement::rowCount(); is not stable
    // across all drivers, so we simply pass the array to php's count() instead
    $this->row_count = count($this->result);
    $this->template->message("Rows: $this->row_count");
    if ($this->result) {
      $this->print_result();
    }
  }

  protected function print_result () {
    $this->fields = array();
    $this->template->table_full_width_start();
    $this->template->table_row_start();
    // gather and print field names by iterating through first result row
    foreach ($this->result[0] as $field => $val) {
      array_push($this->fields, $field);
      switch ($this->utf_convert) {
        case true;
          $this->template->table_row_header(CharacterConvert::utf_to_norwegian($field));
          break;
        case false;
          $this->template->table_row_header($field);
          break;
      }
    }
    $this->template->table_row_end();
    // print out the query result rows
    for ($i = 0; $i < $this->row_count; $i++) {
      $row = $this->result[$i];
      $this->template->table_row_start();
      for ($j = 0; $j < $this->field_count; $j++) {
        switch ($this->utf_convert) {
          case true;
            $this->template->table_row_value(CharacterConvert::utf_to_norwegian($row[$this->fields[$j]]));
            break;
          case false;
            $this->template->table_row_value($row[$this->fields[$j]]);
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
    $port = $this->environment->datawarehouse('barcode_generator_port');
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
    $port = $this->environment->datawarehouse('barcode_generator_port');
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


class GenerateLabelDummySheet extends Developing {
  public function run () {
    // just a working proof of concept for now, will change this
    $host = $this->environment->datawarehouse('barcode_generator_host');
    $port = $this->environment->datawarehouse('barcode_generator_port');
    $api = 'shelf/';
    $url = "http://$host:$port/$api";
    $data = [
      'barcodes' => [
        "A-A-1", "A-A-2", "A-A-3", "A-A-4", "A-A-5", "A-A-6",
        "A-A-7", "A-A-8", "A-A-9", "A-A-10", "A-A-11", "A-A-12",
        "A-A-13", "A-A-14", "A-A-15", "A-A-16", "A-A-17", "A-A-18",
        "A-A-19", "A-A-20", "A-A-21", "A-A-22", "A-A-23", "A-A-24",
        "A-A-25", "A-A-26", "A-A-27", "A-A-28", "A-A-29", "A-A-30",
        "A-A-31", "A-A-32", "A-A-33", "A-A-34", "A-A-35", "A-A-36",
      ],
      'caller' => $this->environment->datawarehouse('cip_info_host'),
    ];
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($curl);
    $http_status_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    if (curl_errno($curl)) {
      if ( $this->environment->developement('show_debug') ) {
        echo 'http status code: ' . $http_status_code;
        die('Error on curl request: ' . curl_error($curl));
      }
    }
    curl_close ($curl);
    if ($http_status_code == 201) {
      header('Content-Type: image/png');
      header('Content-Type: application/octet-stream');
      header('Content-Transfer-Encoding: binary');
      header('Content-Disposition: attachment; filename=shelfdummysheet.png');
      echo $body;
    }
  }
}
