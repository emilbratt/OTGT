<?php

require_once '../applications/Template.php';

class TemplateMap extends Template {

  protected $image_path_floor;

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
      height: 25px;
    }
    a button:hover {
      background-color: $this->colour_default_hover;
    }
    EOT;
  }

  public function map_form_location () {
    $location = '';
    if (isset($_GET['input_field_location'])) {
      $location = $_GET['input_field_location'];
    }
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 400px;">
      <form method="GET">
        <table>
        <tr>
          <td style="width: 30%;">
            <input style="width: 100%;"
            type="search" autofocus="autofocus" onfocus="this.select()"
            id="input_field_location" name="input_field_location"
            placeholder="Lagerplass" value="$location">
          </td>
          <td style="width: 10%;">
            <input style="width: 100%;" type="submit" value="Finn" >
          </td>
        </tr>
        </table>
      </form>
    </div><br>\n
    EOT;
  }

  public function image_map ($name) {
    $this->css .= <<<EOT
    .image_map {
      display: block;
      /*
      margin-left: auto;
      margin-right: auto;
      */
      width: 50%;
    }\n
    EOT;

    $image = $this->image_path_floor . "/$name.png";
    $b64image = base64_encode(file_get_contents($image));
    $this->html .= <<<EOT
    <div class="image_map">
    <img src="data:image/png;base64,$b64image">
    </div>\n
    EOT;
  }

}
