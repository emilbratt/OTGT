<?php

class Template {

  // protected gives the inherited object access to this
  protected $html;

  function __construct () {
    $this->html = <<<EOT
    <!DOCTYPE html>
    <html>\n
    EOT;

  }

  public function print () {
    echo $this->html;
    $this->html = '';
  }

  public function start () {
    $this->html .= <<<EOT
    <style>
    html {
      min-height: 100%;
    }
    body {
      background: linear-gradient(#222222, #000000);
      color: #BBBBFF;
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
    #searchField {
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
    </style>
    <body>\n
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

  public function table_header_value ($string) {
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

}
