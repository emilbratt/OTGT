<?php

require_once '../applications/Template.php';

class TemplateExample extends Template {

  protected $image_path_floor;

  function __construct () {
    parent::__construct();
    $this->image_path_floor = $this->image_path . '/location/floor';
  }

  public function some_text_for_subdirone () {
    $this->html .= <<<EOT
    <p>this is some text for app one</p>\n
    EOT;
  }

}
