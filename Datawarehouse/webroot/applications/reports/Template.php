<?php

class Template {

  private $html;

  function __construct () {
    $this->html = <<<EOT
    <!DOCTYPE html>
    EOT;

  }

  public function print () {
    echo $this->html;
    $this->html = '';
  }

  public function start () {
    $this->html .= <<<EOT
    \n<html>
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
    <body>
    EOT;
  }


  public function title_left ($string = 'left title') {
    $this->html .= '<h1 style="float: left;">' . $string . '</h1>';

  }

  public function title_right ($string = 'right title') {
    $this->html .= '<h1 style="float: right;"> '. $string . '</h1>';
  }


  public function table_start () {
    $this->html .= <<<EOT
    \n<table>
    EOT;
  }

  public function table_row_start () {
    $this->html .= <<<EOT
    \n<tr>
    EOT;
  }

  public function table_header_value ($string) {
    $this->html .= <<<EOT
    \n<th>$string</th>
    EOT;
  }

  public function table_row_value ($string) {
    $this->html .= <<<EOT
    \n<td>$string</td>
    EOT;
  }

  public function table_row_end () {
    $this->html .= <<<EOT
    \n</tr>
    EOT;
  }

  public function table_end () {
    $this->html .= <<<EOT
    \n</table>
    EOT;
  }

  public function end () {
    $this->html .= <<<EOT
    \n</body>
    </html>
    EOT;
  }

}
