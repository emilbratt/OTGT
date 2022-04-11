<?php

/**
 *
 * NOTE:
 *  deprecate date stuff and move to Date.php
 *  create own file for UserAgent and CharacterConvert
 *
 */

class Dates {

  public static function get_this_weekday () {
    $days = array('Søndag', 'Mandag', 'Tirsdag', 'Onsdag','Torsdag','Fredag', 'Lørdag');
    return $days[date('w')];
  }

  public static function get_this_month () {
    $months = [
      'Jan' => 'januar',
      'Feb' => 'februar',
      'Mar' => 'mars',
      'Apr' => 'april',
      'May' => 'mai',
      'Jun' => 'juni',
      'Jul' => 'juli',
      'Aug' => 'august',
      'Sep' => 'september',
      'Oct' => 'oktober',
      'Nov' => 'november',
      'Des' => 'desember',
    ];
    return $months[date('M')];
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
