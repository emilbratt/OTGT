<?php

require_once '../applications/Template.php';

class TemplateReports extends Template {

  function __construct () {
    parent::__construct();
  }

  public function reports_form_input_date () {
    $this->css .= <<<EOT
    .reports_form_input_date {
      display: block;
    }
    EOT;
    $_date = date("Y-m-d");
    $this->html .= <<<EOT
    <div class="reports_form_input_date">
    <form method="GET">
    <input
      type="date"
      value="$_date"
      min="2011-01-01"
      name="type">

    <input
      type="submit"
      value="Velg Dato" >
    </form>
    </div>
    EOT;
  }

}
