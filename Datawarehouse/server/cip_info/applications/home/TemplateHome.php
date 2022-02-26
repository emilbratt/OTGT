<?php

require_once '../applications/Template.php';

class TemplateHome extends Template {
  // methods with same name here will override the method in Template

  function __construct () {
    parent::__construct();
  }

  public function start () {
    $this->html .= <<<EOT
    </style>
    <body>\n
    EOT;
  }

  public function title_left ($string = 'left title') {
    $this->html .= <<<EOT
    <h1 style="float: left;">$string</h1>\n
    EOT;

  }

  public function title_right ($string = 'right title') {
    $this->html .= <<<EOT
    <h1 style="float: right;">$string</h1>\n
    EOT;
  }

}
