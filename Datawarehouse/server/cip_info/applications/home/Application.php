<?php

class Home {

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Database.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/reports/ReportTemplate.php';
    require_once '../applications/reports/QueryReports.php';

  }

  public function run () {
    echo 'this is home served from applications -> Home';
  }
}
