<?php


/**
 *
 * THIS IS THE NAVIGATION PART WHERE MENUS WILL BE CREATED
 * IT INHERITS THE MAIN MENUS FROM ../applications/Navigation.php
 *
 */

require_once '../applications/Navigation.php';

class NavigationExample extends Navigation {
  /**
   *
   * PASS THE ENVIRONMENT CONFIG VARIABLE SO THAT IT CAN DYNAMICALLY
   * ADD OR REMOVE MENU ENTRIES BASED ON THE ENVIRONMENT
   *
   */
  function __construct ($environment) {
    parent::__construct($environment);
    /**
     *
     * SET THE CORRECT NAME FOR THE PAGE (AS FOUND IN application.php)
     * TO PRESERVE THE CORRECT APPLICATION ADDRESS
     *
     */
    $this->home_sub = $this->top_nav_links['Eksempel'];
    /**
     *
     * OPTIONALLY ADD A SUB NAVIGATION MENU THAT APPEARS UNDER THE
     * TOP NAVIGATION BAR
     *
     */
      $this->sub_nav_links = [
      'Sub directory 1' => $this->home_sub . '/subdirone',
      'Sub directory 2' => $this->home_sub . '/subdirtwo',
      'Sub directory 3' => $this->home_sub . '/subdirthree',
    ];
    /*
     *
     * THIS MEANS WE NEED TO ADD CORRESPONDING CLASSES IN Application.php
     * WITH SAME NAME (INCLUDING UPPERCASE CLASS NAMING CONVENTION)
     *
     */
  }

}
