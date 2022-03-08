<?php

require_once '../applications/Template.php';

class TemplateAbout extends Template {

  function __construct () {
    parent::__construct();
    $this->image_path_floor = $this->image_path . '/location/floor';
  }

}
