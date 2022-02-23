<?php

require_once '../applications/Template.php';

class TemplateFind extends Template {
  // methods with same name here will override the method in Template

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
    title {
      display: inline-block;
    }
    table, th, td {
      border:1px solid black;
    }
    th {
      font-size:110%;
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
    form, input {
      display: inline;
      width:250px;
      height: 30px;
    }
    #input_field_brand {
      display: inline;
      width:250px;
      height: 30px;
    }
    #input_field_article {
      display: inline;
      width:650px;
      height: 30px;
    }
    #input_field_div {
      display: inline;
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
    a {
      text-decoration:none
      font-family: arial;
      color: #CCCCFF;

    }
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

  public function form_search ($brand = '', $article = '') {
    $this->html .= <<<EOT

    <div id="input_field_div">
      <form action="">
        <label for="input_field_brand">Merke:</label>
        <input
          type="text" autofocus="autofocus" onfocus="this.select()"
          id="input_field_brand" name="input_field_brand"
          value="$brand">

        <label for="input_field_article">Artikkel:</label>
        <input
          type="text" id="input_field_article" name="input_field_article"
          value="$article">

        <input type="submit" value="Søk">

      </form>
    </div>
    <br><br>\n
    EOT;
  }

  public function message ($string) {
    $this->html .= <<<EOT
    <div class="message">
      <h3>$string</h3>
    </div>\n
    EOT;
  }


}
