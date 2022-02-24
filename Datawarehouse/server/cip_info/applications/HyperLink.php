<?php

/*
 *
 * this is ment to handle dynamic links based on interaction by
 * the visitor and what content is presented
 *
 */

class HyperLink {
  public $url; // example: http://hostname:8080/some/where?foo=bar&this=that
  protected $home_address; // example: http://hostname:8080
  protected $query_string; // example: foo=bar&this=that

  function __construct () {
    $this->url = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    $this->home_address =  $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . '/';
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
    $this->url = $this->home_address . $this->query_string;

    // fix ? instead of & after redirect url
    $val = $_SERVER['REDIRECT_URL'];
    $serch = $_SERVER['REDIRECT_URL'] . '&';
    $replace =  $_SERVER['REDIRECT_URL'] . '?';
    // $this->url = preg_replace('~' . $val . '&~', $val . '?', $this->url);
    $this->url = preg_replace("~$serch~", $replace, $this->url);

  }

  public function link_home ($key = null, $val = null) {
    if($key !== null and $val !== null) {
      $this->url = $this->home_address;
      return;
    }
    $this->url = $this->home_address . '?' . "$key=$val";
  }

  public function link_redirect ($redirect = '/home/home') {
    // redirect example: /reports/imported
    $this->url = $this->home_address . $redirect;
  }

  public function link_redirect_query ($redirect = '/home/home', $key = null, $val = null) {
    // redirect example: /reports/imported
    // optionally add a key value as a query string for eaxmple: $key = 'foo' and $val = 'bar'
    if($key === null or $val === null) {
      $this->url = $this->home_address . $redirect;
      return;
    }
    $this->url = $this->home_address . $redirect . '?' . "$key=$val";
  }

  public function link_redirect_multi_query ($redirect = '/home/home', $query_string = null) {
    // redirect example: /reports/imported
    // query string example; foo=bar&this=that
    if($query_string === null) {
      $this->url = $this->home_address . $redirect;
      return;
    }
    $this->url = $this->home_address . $redirect . '?' . "$query_string";
  }

}
