<?php
/**
 * colours
 * text, boarders: BBBBFF
 * top nav bar active, hover, table row
 * a href CCCCFF
 * search field background 202020
 * table row (even) 222222
 * table row (odd) 333333
 * location circle 9FDF9F
 */


class Template {

  protected $config;
  protected $declaration;
  protected $html;
  protected $css;
  protected $script;
  protected $image_path = '../assets/image';
  private $wrapper; // wraps all individual parts (css, html and scripts)

  function __construct () {
    $config_file = '../../../../environment.ini';
    $this->config = parse_ini_file($config_file, $process_sections = true);
    // this will add global css to our html template
    // any additional css will have to be added after the
    // constructor for each inherited class after
    // calling this as a parent in the inherited constructor method
    $this->declaration = <<<EOT
    <!DOCTYPE html>
    EOT;

    $this->css = <<<EOT
    html {
      min-height: 100%;
    }
    body {
      font-family: arial;
      /* background: linear-gradient(#222222, #000000); */
      background-color: #202020;
      color: #BBBBFF;
    }
    a {
      text-decoration: none;
      font-family: arial;
      color: #CCCCFF;
    }
    a button:hover {
      background-color: #444444;
    }

    .message {
      width: 100%;
      color: #BBBBFF;
      font-size: 18px;
    }

    /* TOP NAVIGATION */
    .top_navbar {
      margin-left: auto;
      margin-right: auto;
      background-color: #303030;
      overflow: hidden;
      width: 100%; /* Full width */
    }
    .top_navbar a {
      /* clickable area */
      float: left;
      color: #BBBBFF;
      text-align: center;
      padding: 14px 16px;
      font-size: 17px;
    }
    .top_navbar a:hover {
      background-color: #444444;
    }
    .top_navbar a.active {
      background-color: #444444;
    }

    /* SUB NAVIGATION */
    .sub_navbar {
      /* background: linear-gradient(#303030, #242424); */
      background-color: #303030; */
      overflow: auto;
      width: 100%;
      color: #BBBBFF;
    }
    .sub_navbar a {
      display: block;
      padding: 14px;
    }
    /* hover colour */
    .sub_navbar a:hover {
      background-color: #444444;
    }
    .sub_navbar a.active {
      background-color: #444444;
    }

    .title {
      display: inline-block;
    }

    .title_left {
      display: inline-block;
      margin-left: 10px;
    }

    .title_right {
      display: inline-block;
      margin-right: 10px;
    }

    /* FORM */
    .template_form {
      width: 700px;
    }
    form, input {
      display: inline;
      width:250px;
      height: 26px;
    }
    input[type="date"] {
      /* somehow this will be same hight as 26px.. */
      height: 22px;
    }
    input[type="text"], input[type="search"], input[type="date"] {
      background-color : #202020;
      color: #BBBBFF;
      border: 1px solid #BBBBFF;
    }
    form input:hover {
      background-color: #444444;
    }
    input[type="submit"] {
      border: 1px solid #BBBBFF;
      display: block;
      color: #BBBBFF;
      background: #222222;
    }

    /* TABLE */
    table {
      font-family: arial;
      border-collapse: collapse;
    }
    .full_width_table {
      width: 100%;
    }
    td {
      border: 1px solid #202020;
      text-align: left;
      padding-left: 2px;
    }
    th {
      background-color: #303030;
      height: 32px;
    }
    th a {
      height: 27px;
      font-size: 20px;
    }
    tr:nth-child(even) {
      background-color: #333333;
    }
    tr:nth-child(odd) {
      background-color: #222222;
    }

    #hidden_submit {
      display: none;
    }
    #input_field_div {
      display: block;
    }
    #search_field {
      background: #202020;
      display: inline-block;
    }
    button {
      border: 1px solid #BBBBFF;
      display: inline;
      font-size: 15px;
      color: #BBBBFF;
      background: #222222;
      width: 150px;
      height: 30px;
    }\n
    EOT;
  }

  public function top_navbar ($arr, $page = 'Hjem') {
    $this->html .= <<<EOT
    <div class="top_navbar" id="top_navbar">\n
    EOT;
    foreach ($arr as $title => $redirect) {
      if ($title == $page) {
        $redirect .= '" class="active';
      }
      $this->html .= <<<EOT
        <a href="$redirect">$title</a>\n
      EOT;
    }
    $this->html .= <<<EOT
    </div>\n
    EOT;
  }

  public function sub_navbar ($arr) {
    $this->html .= <<<EOT
    <div class="sub_navbar">\n
    EOT;
    foreach ($arr as $title => $redirect) {
      $this->html .= <<<EOT
        <a href="$redirect">$title</a>\n
      EOT;
    }
    $this->html .= <<<EOT
    </div>\n
    EOT;
  }

  public function title ($string = 'title') {
    $this->html .= <<<EOT
    <div class="title">
      <h1>$string</h1>
    </div>\n
    EOT;
  }

  public function message ($string) {
    $this->html .= <<<EOT
    <div class="message">
      <p><i>$string</i></p>
    </div>\n
    EOT;
  }

  public function hyperlink_button ($string, $hyperlink) {
    $this->html .= <<<EOT
    <a href="$hyperlink">
      <button >$string</button>
    </a>\n
    EOT;
  }

  public function title_left_and_right ($left = 'left', $right = 'right') {
    $this->html .= <<<EOT
    <div style="width: 100%;">
    <table class="full_width_table">
    <tr>
      <td style="border:none; text-align: left; background-color: #202020;">
        <h1 style="display: inline; width: 100%;">$left</h1>
      </td>
      <td style="border:none; text-align: right; background-color: #202020;">
        <h1 style="display: inline; width: 100%;">$right</h1>
      </td>
    </tr>
    </table>
    </div>\n
    EOT;
  }

  public function form_start ($method = 'GET') {
    $this->html .= <<<EOT
    <div id="template_form">
    <form method="$method">
    <table>
    <tr>\n
    EOT;
  }

  public function form_input_search ($ref = 'form_input_search') {
    // $ref = what key to reference in GET / POST array
    $this->html .= <<<EOT
    <td>
      <input
        type="search"
        id="form_input_search"
        name="$ref">
    </td>\n
    EOT;
  }

  public function form_input_text ($ref = 'form_input_text') {
    // $ref = what key to reference in GET / POST array
    $this->html .= <<<EOT
    <td>
      <input
         type="search"
         id="form_input_text"
         name="$ref">
    </td>\n
    EOT;
  }

  public function form_input_date ($ref = 'form_input_date') {
    // $ref = what key to reference in GET / POST array
    $this->html .= <<<EOT
    <td>
      <input
        type="date"
        id="form_input_date"
        value="2018-07-22"
        min="2018-01-01" max="2018-12-31"
        name="$ref">
    </td>\n
    EOT;
  }

  public function form_end ($val = 'Enter') {
    $this->html .= <<<EOT
    <td>
      <input
        type="submit"
        value="$val" >
    </td>
    </tr>
    </table>
    </form>
    </div><br>\n
    EOT;
  }

  public function table_start () {
    $this->html .= <<<EOT
    <table id="find_item">\n
    EOT;
  }

  public function table_full_width_start () {
    $this->html .= <<<EOT
    <table class="full_width_table" id="find_item">\n
    EOT;
  }

  public function table_row_start () {
    $this->html .= <<<EOT
    <tr>\n
    EOT;
  }

  public function table_row_header ($string, $hyperlink = null) {
    // passing a url as second arg will make it a clickabel button
    if ($hyperlink == null) {
      $this->html .= <<<EOT
      <th>$string</th>\n
      EOT;
      return;
    }
    $this->html .= <<<EOT
    <th>
      <a href="$hyperlink">
        <button style="width: 100%; font-size: 20px;" id="input_field_submit">$string</button>
      </a>
    </th>\n
    EOT;
  }

  public function table_row_value ($string, $hyperlink = null) {
    // passing a url as second arg will make it a clickabel button
    if ($hyperlink == null) {
      $this->html .= <<<EOT
      <td>$string</td>\n
      EOT;
      return;
    }
    $this->html .= <<<EOT
    <td>
      <a href="$hyperlink">
        <button style="width: 100%; font-size: 20px;" id="input_field_submit">$string</button>
      </a>
    </th>\n
    EOT;
  }

  public function table_row_end () {
    $this->html .= <<<EOT
    </tr>\n
    EOT;
  }

  public function table_end () {
    $this->html .= <<<EOT
    </table>\n
    EOT;
  }

  public function script_filter_row_button ($col_index = '1') {
    // filter (remove rows) from a html table by searching string in this box
    $this->html .= <<<EOT
    <input style="width: 30%;" type="text" id="filter_row" onkeyup="filter_row()" placeholder="Filtrer" title="Type in a name">
    EOT;
    $this->script .= <<<EOT
    function filter_row() {
      var input, filter, table, tr, td, i, text_val;
      input = document.getElementById("filter_row");
      filter = input.value.toUpperCase();
      table = document.getElementById("find_item");
      tr = table.getElementsByTagName("tr");
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[$col_index];
        if (td) {
          text_val = td.textContent || td.innerText;
          if (text_val.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
      }
    }\n
    EOT;
  }

  public function print () {
    $this->wrapper = "$this->declaration\n";
    $this->wrapper .= <<<EOT
    <html>
    <style>
    $this->css
    </style>

    <body>\n
    EOT;

    if($this->config['developement']['show_debug']) {
      $this->add_debug();
    }

    $this->wrapper .= <<<EOT
    $this->html
    <script>
    $this->script
    </script>
    </body>
    </html>\n
    EOT;

    echo $this->wrapper;
  }

  private function add_debug () {
    // custom debug material can be added here
    $this->html .= <<<EOT
    <br><br>
    <p>------------------------------------------</p>
    <p>-------- Debug Enabled --------</p>
    <p>------------------------------------------</p>\n
    EOT;
    $this->html .= <<<EOT
    <p>\$_SERVER</p>
    <pre>\n
    EOT;
    foreach ($_SERVER as $key => $val) {
      $this->html .= "$key --> $val\n";
    }
    $this->html .= <<<EOT
    </pre>\n
    EOT;
    $this->html .= <<<EOT
    <p>\$_GET</p>
    <pre>
    EOT;
    if (isset($_GET)) {
      foreach ($_GET as $key => $val) {
        $this->html .= "$key --> $val\n";
      }
    }
    $this->html .= <<<EOT
    </pre>\n
    EOT;
  }

  function __destruct () {

  }

}
