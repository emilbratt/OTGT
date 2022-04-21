<?php

require_once '../applications/Template.php';

class TemplateDeveloping extends Template {

  function __construct () {
    parent::__construct();
    $this->image_path_floor = $this->image_path . '/location/floor';
    $this->css .= <<<EOT
    .sql_shell_form {
      background-color: #202020;
      color: #BBBBFF;
    }
    /* TABLE */
    table {
      font-family: arial;
      border-collapse: collapse;
    }
    td {
      border: 1px solid #202020;
      text-align: left;
      padding-left: 2px;
    }
    th {
      background-color: $this->colour_header_background;
      height: 32px;
    }
    #th_no_hyperlink {
      border: 1px solid $this->colour_default_text;
    }
    tr:nth-child(even) {
      background-color: $this->colour_row_background_2;
    }
    tr:nth-child(odd) {
      background-color: $this->colour_row_background_1;
    }
    button {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      width: 150px;
      height: 30px;
    }

    /* show image from bytestream */
    .image_show {
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 40%;
    }\n
    EOT;
  }

  public function sql_shell_form ($query) {

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
