<?php


class Instructions {

  protected $page = 'Instrukser'; // alias for top_navbar
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/Environment.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/instructions/TemplateInstructions.php';
    require_once '../applications/instructions/NavigationInstructions.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationInstructions($this->environment);
    $this->template = new TemplateInstructions();
  }

}


class Home extends Instructions {

  public function run () {
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
    $this->template->title('Instrukser');
    $this->template->message('her skal det komme instrukser');
    $this->template->print();
  }

}
