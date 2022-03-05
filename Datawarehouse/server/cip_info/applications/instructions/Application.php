<?php


class Instructions {

  protected $page = 'Instrukser'; // alias for top_navbar
  protected $template;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/instructions/TemplateInstructions.php';
    require_once '../applications/instructions/NavigationInstructions.php';

    $this->template = new TemplateInstructions();
  }

}


class Home extends Instructions {

  public function run () {
    $navigation = new NavigationInstructions();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
    $this->template->title('Instrukser');
    $this->template->message('her skal det komme instrukser');
    $this->template->print();
  }

}
