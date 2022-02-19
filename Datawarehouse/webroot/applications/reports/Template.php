<?php

class Template {


  public static function doc_head () {
    return <<<EOT
    <!DOCTYPE html>
    <html>
    EOT;
  }

  public static function doc_style () {
    return <<<EOT
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
    EOT;
  }

  public static function doc_start () {
    return <<<EOT
    <body>
    EOT;
  }

  public static function doc_end () {
    return <<<EOT
    </body>
    </html>
    EOT;
  }


  public static function doc_title_left ($string) {
    return '<h1 style="float: left;">' . $string . '</h1>';

  }

  public static function doc_title_right ($string) {
    return '<h1 style="float: right;"> '. $string . '</h1>';
  }
}
