<?php
/**
 * colours
 * text: BBBBFF
 * top nav bar active / hover 404040
 * a href CCCCFF
 * search field background 111111
 * table row (even) 222222
 * table row (odd) 333333
 */


class Template {

  // protected gives the inherited object access to this
  protected $config;
  protected $html;
  protected $script;

  function __construct () {
    $config_file = '../../../../environment.ini';
    $this->config = parse_ini_file($config_file, $process_sections = true);
    // this will add global css to our html template
    // any additional css will have to be added after the
    // constructor for each inherited class after
    // calling this as a parent
    $this->html = <<<EOT
    <!DOCTYPE html>
    <html>
    <style>
    html {
      min-height: 100%;
    }
    body {
      background: linear-gradient(#222222, #000000);
      color: #BBBBFF;
    }
    a {
      text-decoration: none;
      font-family: arial;
      color: #CCCCFF;
    }

    /* TOP NAVIGATION */
    .top_navbar {
      background-color: #303030;
      overflow: hidden;
    EOT;
    if(!($this->config['developement']['show_debug'])) {
      // this hides the internal error warnings from php that shows on top of page
      // therefore we only activate this css if debug in environment = false
      $this->html .= <<<EOT
      position: fixed; /* force to stay on same place */
      top: 0;
      transition: top 0.3s; /* hide/dhow transition effect from script call in seconds */
      margin-bottom: 50px;
      EOT;
    }
    $this->html .= <<<EOT
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
      background-color: #404040;
    }
    .top_navbar a.active {
      background-color: #404040;
    }

    /* SUB NAVIGATION */
    .sub_navbar {
      background-color: #303030;
      overflow: auto;
      width: 200px;
      color: #BBBBFF;
    }
    .sub_navbar a {
      display: block;
      padding: 14px;
    }
    /* hover colour */
    .sub_navbar a:hover {
      background-color: #404040;
    }
    .sub_navbar a.active {
      background-color: #404040;
    }

    .title {
      display: inline-block;
    }
    table, th, td {
      border:1px solid black;
    }
    table {
      font-family: arial;
      border-collapse: collapse;
      opacity: 0.8;
      width: 100%;
    }
    td {
      text-align: right;
    }
    input[type="text"], input[type="search"] {
      background-color : #111111;
      color: #BBBBFF;
      border: 1px solid #AAAAAA;
    }
    #form_barcode  {
      font-size: 150%;
      text-align: center;
    }
    form {
      padding-bottom: 10px;
    }
    form, input {
      width:250px;
      height: 30px;
    }
    form, input {
      display: inline;
      width:250px;
      height: 26px;
    }
    #search_field {
      background: #111111;
      display: inline-block;
    }
    td, th {
      border: 1px solid #111111;
      text-align: left;
      padding-left: 2px;
    }
    tr:nth-child(even) {
      background-color: #222222;
    }
    tr:nth-child(odd) {
      background-color: #333333 ;
    }
    #input_field_div {
      display: inline;
    }
    input[type="submit"], button {
      display: inline;
      color: #BBBBFF;
      background: #222222;
      display: inline;
      width: 150px;
      height: 30px;
    }
    #input_field_article {
      display: inline;
      width: 400px;
    }
    #input_field_brand {
      display: inline;
      width: 170px;
    }\n
    EOT;
  }

  protected function add_script () {
    $this->html .= $this->script;
    $this->script = '';
  }

  public function start () {
    // when the style is added, we call this function to start
    // adding html content to the body tag
    $this->html .= <<<EOT
    </style>
    <body>\n
    EOT;
  }

  public function top_navbar ($arr, $page = 'Hjem') {
    // the $page var indicates current page -> link is highlighted
    $this->script .= <<<EOT
    <script>
    var prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
      var currentScrollPos = window.pageYOffset;
      if (prevScrollpos > currentScrollPos) {
        document.getElementById("top_navbar").style.top = "0";
      } else {
        document.getElementById("top_navbar").style.top = "-50px";
      }
      prevScrollpos = currentScrollPos;
    }
    </script>
    EOT;
    $this->add_script();
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
    </div>
    EOT;
    if(!($this->config['developement']['show_debug'])) {
      // this hides the internal error warnings from php that shows on top of page
      // therefore we only activate this css if debug in environment = false
      $this->html .= <<<EOT
      <!-- we have to add some empty space to force next html tag to show -->
      <div style="height: 50px;"></div> \n
      EOT;
    }

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
    </div>
    <br> <!-- br tag for forcing the next html objects to start from under the top nav -->\n
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
      <h3>$string</h3>
    </div>\n
    EOT;
  }

  public function hyperlink ($string, $hyperlink) {
    $this->html .= <<<EOT
    <a href="$hyperlink">
      <button id="input_field_submit">$string</button>
    </a>\n
    EOT;
  }

  public function title_left ($string = 'left title') {
    $this->html .= <<<EOT
    <h1 style="float: left;">$string</h1>\n
    EOT;
  }

  public function title_right ($string = 'right title') {
    $this->html .= <<<EOT
    <h1 style="float: right;">$string</h1>\n
    EOT;
  }


  public function table_start () {
    $this->html .= <<<EOT
    <table>\n
    EOT;
  }

  public function table_row_start () {
    $this->html .= <<<EOT
    <tr>\n
    EOT;
  }

  public function table_row_header ($string) {
    $this->html .= <<<EOT
    <th>$string</th>\n
    EOT;
  }

  public function table_row_value ($string) {
    $this->html .= <<<EOT
    <td>$string</td>\n
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

  public function print () {

    // only if debugging is set, we show php globals
    if($this->config['developement']['show_debug']) {
      $this->add_debug();
    }
    // print out the final html template as the last step
    $this->html .= <<<EOT
    </body>
    </html>
    EOT;
    echo $this->html;
    $this->html = null;
  }


  private function add_debug () {
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
    foreach ($_GET as $key => $val) {
      $this->html .= "$key --> $val\n";
    }
    $this->html .= <<<EOT
    </pre>\n
    EOT;
  }

  function __destruct () {

  }

}
