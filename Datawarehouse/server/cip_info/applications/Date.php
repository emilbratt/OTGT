<?php

class Date {

  public $year;
  public $month;
  public $day;
  public $display;
  public $date_time;
  public $unix_time_stamp;
  public $yyyymmdd;
  public $date;
  public $time;

  function __construct () {
    $this->date_time = date('Y-m-d_H:i:s');
    $this->unix_time_stamp = time();
    $this->yyyymmdd = date('Ymd');
    $this->display = date('d').'-'.date('m').'-'.date('Y');
  }

  public function read_string ($string) {
    $this->year = date('Y', strtotime($string));
    $this->month = date('m', strtotime($string));
    $this->day = date('d', strtotime($string));
  }

  public function format_from_string ($string) {
    $this->year = date('Y', strtotime($string));
    $this->month = date('m', strtotime($string));
    $this->day = date('d', strtotime($string));
    $this->display = $this->day.'-'.$this->month.'-'.$this->year;
  }

  public function date_from_time_stamp ($string = null) {
    if ($string === null) {
      $string = date('Y-m-d H:i:s');
    }
    return date('Y-m-d', strtotime($string));
  }

  public function sql_compatible_date ($unix_epoch = null) {
    // takes unix epoch as integer
    if ($unix_epoch === null) {
      $unix_epoch = time();
    }
    return date('Y-m-d', $unix_epoch);
  }

  public function sql_compatible_time ($unix_epoch = null) {
    // takes unix epoch as integer
    if ($unix_epoch === null) {
      $unix_epoch = time();
    }
    return date('H:i:s', $unix_epoch);
  }

}
