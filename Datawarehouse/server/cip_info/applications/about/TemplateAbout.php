<?php

require_once '../applications/Template.php';

class TemplateAbout extends Template {

  function __construct () {
    parent::__construct();
    $this->image_path_floor = $this->image_path . '/location/floor';

    $this->css .= <<<EOT
    a button {
      border: 1px solid $this->colour_default_border;
      display: block;
      color: $this->colour_default_text;
      background: $this->colour_input_background;
    }
    a button:hover {
      background-color: $this->colour_default_hover;
    }\n
    EOT;
  }

}
