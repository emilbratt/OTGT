<?php

class Home {

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Helpers.php';
    require_once '../applications/home/HomeTemplate.php';

  }

  public function run () {
    $weekday = Dates::get_this_weekday();
    echo "Dette er 'home' og i dag er det $weekday";
  }

}
