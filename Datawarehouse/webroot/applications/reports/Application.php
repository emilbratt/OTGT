<?php

/*
notes:
for turnover reports, maybe include graphs using some graphing tool for web view

*/

class Home {
  function __construct () {

    $reports = [
      'Utsolgt idag' => '/reports/soldout/today',
      'Utsolgt denne uken' => '/reports/soldout/week',
    ];
    foreach ($reports as $name => $page) {
      echo '<a href="http://'.$_SERVER['HTTP_HOST'].$page.'">'.$name.'</a><br>';
    }
  }
}

class Soldout {
  function __construct () {
    $page = Pagerequest::get_file('./applications/reports/soldout');
    if($page !== false) {
      require_once $page;
      $page = new Page();
    }
  }
}

class Turnover {
  function __construct () {
    echo 'this is reports - Turnover served from Application.php';
  }
}
