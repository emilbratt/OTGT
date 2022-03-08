<?php
/**
 * colours
 * text, border: BBBBFF
 * top nav bar active, hover, table row
 * a href CCCCFF
 * search field background 202020
 * table header 2A2A2A (unless clickable hyperlink)
 * table row (even) 222222
 * table row (odd) 333333
 * location circle 9FDF9F
 */


class Template {

  protected $colour_page_background = '#202020';
  protected $colour_default_background = '#222222';
  protected $colour_default_text = '#BBBBFF';
  protected $colour_default_border = '#BBBBFF';
  protected $colour_default_menu_background = '#303030';
  protected $colour_input_background = '#222222';
  protected $colour_header_background = '#2A2A2A';
  protected $colour_row_background_1 = '#222222';
  protected $colour_row_background_2 = '#333333';
  protected $colour_search_background = '#202020';
  protected $colour_default_hover = '#444444';
  protected $colour_default_active = '#444444';
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
      background-color: $this->colour_page_background;
      color: $this->colour_default_text;
    }
    a {
      text-decoration: none;
      font-family: arial;
      color: #CCCCFF;
    }
    a button:hover {
      background-color: $this->colour_default_hover;
    }

    .message {
      width: 100%;
      color: $this->colour_default_text;
      font-size: 18px;
    }

    /* TOP NAVIGATION */
    .top_navbar {
      margin-left: auto;
      margin-right: auto;
      background-color: $this->colour_default_menu_background;
      overflow: hidden;
      width: 100%; /* Full width */
    }
    .top_navbar a {
      float: left;
      display: inline;
      color: $this->colour_default_text;
      text-align: center;
      padding: 14px 16px;
      font-size: 17px;
    }
    .top_navbar a:hover {
      background-color: $this->colour_default_hover;
    }
    .top_navbar a.active {
      background-color: $this->colour_default_active;
    }

    /* SUB NAVIGATION */
    .sub_navbar {
      background-color: $this->colour_default_menu_background; */
      overflow: auto;
      width: 100%;
      color: $this->colour_default_text;
    }
    .sub_navbar a {
      display: block;
      padding: 14px;
    }
    /* hover colour */
    .sub_navbar a:hover {
      background-color: $this->colour_default_hover;
    }
    .sub_navbar a.active {
      background-color: $this->colour_default_active;
    }

    .title {
      display: block;
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
      background-color: $this->colour_input_background;
      color: $this->colour_default_text;
      border: 1px solid $this->colour_default_border;
    }
    form input:hover {
      background-color: $this->colour_default_hover;
    }
    input[type="submit"] {
      border: 1px solid $this->colour_default_border;
      display: block;
      color: $this->colour_default_text;
      background: $this->colour_input_background;
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
      background-color: $this->colour_header_background;
      height: 32px;
    }
    #th_no_hyperlink {
      border: 1px solid $this->colour_default_text;
    }
    th a {
      height: 27px;
      font-size: 20px;
    }
    tr:nth-child(even) {
      background-color: $this->colour_row_background_2;
    }
    tr:nth-child(odd) {
      background-color: $this->colour_row_background_1;
    }

    #hidden_submit {
      display: none;
    }
    #input_field_div {
      display: block;
    }
    #search_field {
      background-color: $this->colour_search_background;
      display: inline-block;
    }
    button {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      width: 150px;
      height: 30px;
    }\n
    EOT;
  }


  public function custom_html ($str) {
    $this->html .= <<<EOT
    $str\n
    EOT;
  }

  public function custom_css ($str) {
    $this->css .= <<<EOT
    $str\n
    EOT;
  }

  public function custom_script ($str) {
    $this->script .= <<<EOT
    $str\n
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
         type="text"
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
      <th id="th_no_hyperlink">$string</th>\n
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

  public function script_filter_row_button ($col_index = '1', $placeholder = 'Filtrer Resultat') {
    // filter (remove rows) from a html table by searching string in this box
    $this->html .= <<<EOT
    <input
      style="width: 30%;"
      type="text"
      id="filter_row"
      onkeyup="filter_row()"
      placeholder="$placeholder"
      title="novalue">
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
