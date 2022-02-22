<?php

/*
 *
 * this is ment to handle dynamic links based on interaction by
 * the visitor and what content is presented
 *
 */

class HyperLink {
  public $url; // example: http://hostname:8080?foo=bar&this=that
  protected $address; // example: http://hostname:8080
  protected $query_string; // example: foo=bar&this=that

  function __construct () {
    $this->url = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    $this->address =  $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . '/';
    $this->query_string = '';
    if(isset($_SERVER['REDIRECT_QUERY_STRING'])) {
      $this->query_string = $_SERVER['REDIRECT_QUERY_STRING'];
    }
  }

  public function add_query ($key, $val) {
    // add query string: http://hostname:8080?foo=bar -> http://hostname:8080?foo=bar&this=that
    // or
    // change query string if key exists: http://hostname:8080?foo=bar -> http://hostname:8080?foo=that

    // first, remove or replace with empty string if key exist
    // regex: starts with either ? or & followed by $key followed by = and any value until & or end of string
    $this->query_string = preg_replace('/(\?|&)'.$key.'=[^&]*/', '', $this->query_string);
    // then add key=val to the end of the query string
    $this->query_string .= '&' . "$key=$val";
    // then change/add query string to our
    $this->url = $this->address . $this->query_string;
  }

}
