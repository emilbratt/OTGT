<?php

/**
 *
 * TODO:
 *  add: feature for uploading instruction in pdf file and place it in a category (remember to add upload dir to gitignore)
 *
 */

class Instructions {

  protected $page = 'Instrukser';
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/instructions/TemplateInstructions.php';
    require_once '../applications/instructions/NavigationInstructions.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationInstructions();
    $this->template = new TemplateInstructions();
  }

}


class Home extends Instructions {

  public function run () {
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
    $this->template->title('Instrukser');
    $this->template->_form_upload_instruction();
    $this->template->print($this->page);
  }

}
