<?php

require_once '../applications/Template.php';

class TemplateDeveloping extends Template {

  function __construct () {
    parent::__construct();
    $this->image_path_floor = $this->image_path . '/location/floor';
    $this->css .= <<<EOT
    button {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      width: 150px;
      height: 30px;
    }\n
    EOT;
  }

  public function sql_shell_form ($query) {
    $this->css .= <<<EOT
    .sql_shell_form {
      background-color: #202020;
      color: #BBBBFF;
    }
    EOT;
    $this->html .= <<<EOT
    <div class="">
    <form action="" method="post">
    <textarea
      name="sql_shell_query"
      rows="25"
      cols="120"
      class="sql_shell_form">$query</textarea>
    <br>
    <input type="submit" value="Execute" style="width:100px">
    </form>
    </div>
    EOT;
  }

}
