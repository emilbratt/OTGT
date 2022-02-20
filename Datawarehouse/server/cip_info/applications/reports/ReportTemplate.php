<?php

require_once '../applications/Template.php';

class ReportTemplate extends Template {
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
    a {
      text-decoration:none
      font-family: arial;
      color: #CCCCFF;

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

  // public function table_row_header ($string, $new_sort) {
  //   $old_sort = $_GET['sort'];
  //   $res = str_replace("sort=$new_sort", "sort=$old_sort", $_SERVER['REQUEST_URI']);
  //   $url =  $_SERVER['HTTP_HOST'].$res;
  //
  //   $this->html .= <<<EOT
  //   <th><a href="$url">$string</a></th>\n
  //   EOT;
  //
  //
  //   // $this->html .= <<<EOT
  //   // <th><a href="sort=Name">$string</a></th>
  //   // <th>$string</th>\n
  //   // EOT;
  // }

  public function for_laaater ($string) {



    $path = explode('&', $_SERVER['REDIRECT_QUERY_STRING'])[0];
    unset($_GET['index_php']);
    unset($_GET[$path]);
    echo '<pre>';
    print_r($_GET);
    echo '</pre>';
    $_GET['sort'] = 'quantity';
    $new_query_string = http_build_query($_GET);
    $path = $_SERVER['REDIRECT_URL'];
    $url =  $_SERVER['HTTP_HOST'].$path. '?' .$new_query_string;


    //
    // $query = $_GET;
    // // replace parameter(s)
    // $query['type'] = 'thismonth';
    // // rebuild url
    // $query_result = http_build_query($query);
    // // new link
    //
    // $doc_root = $_SERVER['HTTP_HOST'].explode('&', $_SERVER['REDIRECT_URL'])[0];
    // $url = "$doc_root/$query_result";
    // echo $url;
    // echo <<<EOT
    // <a href="$doc_root/$query_result">URL</a>
    // EOT;
    // // echo $query_result;
    // die;


    // $doc_root = $_SERVER['HTTP_HOST'].explode('?', $_SERVER['REDIRECT_URL'])[0];
    // $path = explode('&', $_SERVER['REDIRECT_QUERY_STRING'])[0];
    // echo $path; die;

    $doc_root = $_SERVER['HTTP_HOST'] . $_SERVER['REDIRECT_URL'];
    // echo $doc_root;
    $doc_root = parse_url($doc_root, PHP_URL_PATH);
    // $url = "$doc_root/$query_result";
    // echo $doc_root; die;


    echo '<pre>';
    print_r($_SERVER);
    echo '</pre>';
    echo explode('&', $_SERVER['REDIRECT_URL'])[0];
    die;
    // echo http_build_query($data) . "\n";
    $data = http_build_query($data);
    echo $data; die;
    // $this->html .= <<<EOT
    // <th><a href="sort=Name">$string</a></th>
    // <th>$string</th>\n
    // EOT;
  }



}
