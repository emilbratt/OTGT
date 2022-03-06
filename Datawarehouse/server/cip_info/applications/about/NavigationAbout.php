<?php


/**
 *
 * THIS IS THE NAVIGATION PART WHERE MENUS WILL BE CREATED
 * IT INHERITS THE MAIN MENUS FROM ../applications/Navigation.php
 *
 */

require_once '../applications/Navigation.php';

class NavigationAbout extends Navigation {
  /**
   *
   * PASS THE ENVIRONMENT CONFIG VARIABLE SO THAT IT CAN DYNAMICALLY
   * ADD OR REMOVE MENU ENTRIES BASED ON THE ENVIRONMENT
   *
   */
  function __construct ($environment) {
    parent::__construct($environment);
  }

}
