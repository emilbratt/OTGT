<?php

require_once '../applications/Template.php';

class TemplateMap extends Template {

  protected $image_path_floor;

  function __construct () {
    parent::__construct();
    $this->image_path_floor = $this->image_path . '/location/floor';
  }


  public function image_map ($name) {
    $this->css .= <<<EOT
    .center_map {
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 50%;
    }

    EOT;
    $image = $this->image_path_floor . "/$name.png";
    $b64image = base64_encode(file_get_contents($image));
    $this->html .= <<<EOT
    <div class="center_map">
    <img src="data:image/png;base64,$b64image">
    </div>
    EOT;
  }

}
