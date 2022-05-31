<?php

class UserAgent {

  protected $user_agent;

  function __construct () {
    $this->user_agent = $_SERVER["HTTP_USER_AGENT"];
  }

  public function is_mobile () {
    if(preg_match("/(android|iphone|ipod|ipad|phone|tablet|up\.browser|up\.link|wos)/i",$this->user_agent )) {
      return true;
    }
    return false;
  }

}
