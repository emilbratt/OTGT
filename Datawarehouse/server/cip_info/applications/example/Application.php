<?php

/**
 *
 * ABOUT:
 *  this is just an example for showing how to structure the application
 *  for it to work correctly and integrate well with the framework
 *  and should not normally be part of the web-server
 *
 */

class Example {
  /**
   *
   * HERE GOES ALL THE GLOBAL LOGIC FOR THIS SPECIFIC APPLICATION
   * NOTICE HOW THE CLASSES INHERIT FROM THIS MAIN APPLICATION CLASS
   *
   */
  protected $page = 'Eksempel'; // HIGHLIGHTING THE CURRENT PAGE IN TOP NAV BAR
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/example/TemplateExample.php';
    require_once '../applications/example/NavigationExample.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationExample();
    $this->template = new TemplateExample();

    /**
     *
     *  ADD NAVIGATION VALUES TO THE TOP NAV BAR THAT WILL SHOW ON ALL PAGES
     * IN THIS APPLICATION
     *
     */
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}

/**
 *
 *
 * THE APPLICATIONS ENTRYPOINTS STARTING WITH Home ARE FOUND BELOW
 *
 *
 */

class Home extends Example {
  /**
   *
   * THIS IS THE HOME DIRECTORY FOR THIS APPLICATION AND WILL BE
   * LOADED BY DEFAULT UNLESS A SUB STRING IS ADDED TO THE QUERYSTRING
   *
   * THE ADDRESS TO THIS CLASS IS: http://host:port/example
   *
   */
  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $dev_email = $this->environment->contact_dev('email');
    $dev_name = $this->environment->contact_dev('name');
    $this->template->message('This is an example app for developer guidance');
    $this->template->message('Current maintainer of web server: ' . $dev_name);

    $this->template->print();
  }

}


class PageOne extends Example {
  /**
   *
   * THIS IS THE SUBDIRONE DIRECTORY FOR THIS APPLICATION AND WILL BE
   * LOADED BY DEFAULT UNLESS A SUB STRING IS ADDED TO THE QUERYSTRING
   *
   * THE ADDRESS TO THIS CLASS IS: http://host:port/example/pageone
   *
   */
  public function run () {
    // using method from TemplateExample.php
    $this->template->some_text_for_subdirone();
    $this->template->print();
  }
}


class PageTwo extends Example {
  /**
   * THE ADDRESS TO THIS CLASS IS: http://host:port/example/pagetwo
   */
  public function run () {
    $this->template->message('this text is added using the method "message" in the parent class');
    $this->template->print();
  }
}

class PageThree extends Example {
  /**
   * THE ADDRESS TO THIS CLASS IS: http://host:port/example/pagethree
   */
  public function run () {
    $this->template->title_left_and_right('using the parent method for showing left', 'and right title');
    $this->template->print();
  }
}
