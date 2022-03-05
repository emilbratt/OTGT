<?php

/**
 *
 * add: quick input box for barcode scanning
 * add: overview over todays turnover
 * add: diagram
 *
 */

class Home {

  protected $page = 'Hjem'; // alias for top_navbar
  protected $title_left;
  protected $title_right;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Helpers.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/Navigation.php';

    $this->title_left = 'C.I.Pedersen';
    $this->title_right = Dates::get_this_weekday() . ' ' . date("d/m-Y");

    $this->template = new TemplateHome();
    $navigation = new Navigation();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
  }

  public function run () {


    $this->template->title_left_and_right($this->title_left, $this->title_right);

    $this->template->message('denne siden er fremdeles under utvikling');
    $this->template->message('du kan likevel benytte eksisterende funksjoner');
    $this->template->message('jobber nå med å legge inn funksjon for å registrere vareplassering');
    $this->template->message('Emil B. B.');
    $this->template->print();
  }

}
