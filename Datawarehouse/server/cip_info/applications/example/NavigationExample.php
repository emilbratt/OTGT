<?php


/**
 *
 * THIS IS THE NAVIGATION PART WHERE MENUS WILL BE CREATED
 * IT INHERITS THE MAIN MENUS FROM ../applications/Navigation.php
 *
 */

require_once '../applications/Navigation.php';

class NavigationExample extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    /**
     *
     * SET THE CORRECT NAME FOR THE PAGE (AS FOUND IN application.php)
     * TO PRESERVE THE CORRECT APPLICATION URI
     *
     */
    $this->app_uri = $this->top_nav_links['Eksempel'];
    /**
     *
     * ADD A SUB NAVIGATION MENU THAT APPEARS UNDER THE
     * TOP NAVIGATION BAR USINGTHE APPLICATION URI
     *
     */
      $this->sub_nav_links = [
      'Page 1' => $this->app_uri . '/pageone',
      'Page 2' => $this->app_uri . '/pagetwo',
      'Page 3' => $this->app_uri . '/pagethree',
    ];
    /*
     *
     * THIS MEANS WE NEED TO ADD CORRESPONDING CLASSES IN Application.php
     * WITH SAME NAME (INCLUDING UPPERCASE CLASS NAMING CONVENTION)
     *
     */
  }

}
