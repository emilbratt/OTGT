<?php

require_once '../applications/Template.php';

class TemplatePlacement extends Template {

  function __construct () {
    parent::__construct();
  }

  public function css_svg () {
    $this->css .= <<<EOT
      svg{width:30%; height:auto;}
    EOT;
  }

  public function html_svg () {
    $this->html .= <<<EOT
    <svg viewbox="0 0 50 60">
      <polygon points="0 0 50 0 50 5 0 50" fill="#C000FF"/>
      <polygon points="0 50 50 5 50 60 0 60" fill="#803698"/>
    </svg>
    EOT;
  }

}
