<?php

class Template {

  // protected gives the inherited object access to this
  protected $html;

  function __construct () {
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
    title {
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
    input[type="text"] {
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
    #input_field_submit {
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
    }
    a {
      text-decoration: none;
      font-family: arial;
      color: #CCCCFF;
    }\n
    EOT;
  }

  public function start () {
    // when the style is added, we call this function to start
    // adding html content to the body tag
    $this->html .= <<<EOT
    </style>
    <body>\n
    EOT;
  }

  public function title ($string = 'title') {
    $this->html .= <<<EOT
    <div class="title">
      <h1>$string</h1>
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

  public function end () {
    $this->html .= <<<EOT
    </body>
    </html>
    EOT;
  }

  public function print () {
    // print out the final html template as the last step
    echo $this->html;
    $this->html = '';
  }

  function __destruct () {

  }

}
