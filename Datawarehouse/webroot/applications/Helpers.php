<?php


class Dates {

  public static function get_weekday () {
    $days = array('Søndag', 'Madnag', 'Tirsdag', 'Onsdag','Torsdag','Fredag', 'Lørdag');
    return $days[date('w')];
  }
}


class UserAgent {

  public static function is_mobile () {
    $http_user_agent = $_SERVER["HTTP_USER_AGENT"];
    if(preg_match("/(android|iphone|ipod|ipad|phone|tablet|up\.browser|up\.link|wos)/i",$http_user_agent )) {
      return true;
    }
    return false;
  }
}


class CharacterConvert {

  public static function utf_to_norwegian ($string) {
    return mb_convert_encoding($string, "UTF-8", "ISO-8859-1");
  }
}
