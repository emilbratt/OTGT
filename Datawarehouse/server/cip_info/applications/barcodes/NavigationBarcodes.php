<?php

require_once '../applications/Navigation.php';

class NavigationBarcodes extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Strekkoder'];
    $this->sub_nav_links = [
      'Lag Strekkode' => $this->app_uri . '/generatebarcode',
      'Lag QR kode' => $this->app_uri . '/generateqrcode',
      'Lag Hyllemerking' => $this->app_uri . '/generateshelflabels',
    ];
  }

}
