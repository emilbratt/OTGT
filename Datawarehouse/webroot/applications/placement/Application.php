<?php


class Home {
  function __construct () {
    echo 'register item to a specified location';
    require_once './applications/Helpers.php';
    echo '<br>';
    if(UserAgent::is_mobile()) {
      echo 'yes';
      return;
    };
    echo 'no';
  }
}



// register by scanning item, then scanning shelf
// on screen verification should be implemented

class Mobile {
  // if user agent is mobile
}


class Desktop {
  // if user agent is desktop pc
}
