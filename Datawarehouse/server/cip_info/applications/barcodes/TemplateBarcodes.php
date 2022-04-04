<?php

require_once '../applications/Template.php';

class TemplateBarcodes extends Template {

  function __construct () {
    parent::__construct();

    $this->css .= <<<EOT
    button {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      width: 150px;
      height: 25px;
    }\n
    EOT;
  }

  public function _label_form ($sheet_limit) {
    // the sheet_limit must be passed because we need to know the maximum
    // number of shelf labels that can fit on a paper sheet
    $this->html .= <<<EOT
    <div>
    <form enctype="multipart/form-data" method="POST">\n
    EOT;
    for ($i = 1; $i <= $sheet_limit; $i+=2) {
      $odd = strval($i);
      $even = strval($i + 1);
      $this->html .= <<<EOT
      <div>
        <input type="text" name="$odd">
        <input type="text" name="$even">
      </div>\n
      EOT;
    }
    $this->html .= <<<EOT
    <input type="submit" value="Generer">
    </form>
    </div>\n
    EOT;
  }

}
