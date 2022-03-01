<?php

class Date {

  public $year;
  public $month;
  public $day;
  public $display;

  function __construct () {
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
}
