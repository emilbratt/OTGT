<?php

/**
 *
 * TODO:
 *  nothing at the moment
 *
 */

require_once '../applications/Template.php';

class TemplateFind extends Template {

  protected $image_path_location;
  protected $location_index;

  function __construct () {
    parent::__construct();
    $this->image_path_location = $this->image_path . '/location';
    $this->location_index = [
      '1' => '1', 'A' => '1', 'B' => '1',
      '2' => 'U', 'C' => 'U', 'D' => 'U', 'E' => 'U',
      'F' => 'U', 'G' => 'U1', 'H' => 'U1', 'I' => 'U1',
      'J' => 'U1', 'K' => 'U1', 'L' => 'U1', 'M' => 'U1',
      'O' => 'U1', 'P' => 'U1', 'Q' => 'U1', 'R' => 'U1',
      'S' => 'U1', 'T' => 'U1', 'O' => 'U1'
    ];
  }

  public function css_by_search () {
    $this->css .= <<<EOT
    /* set fixed length for each table column */
    td:nth-child(1) {
      width: 10%;
    }
    td:nth-child(2) {
      width: 60%;
    }
    td:nth-child(3) {
      width: 5%;
    }
    td:nth-child(4) {
      width: 7%;
    }
    td:nth-child(5) {
      width: 18%;
    }
    #input_field_article {
      display: inline;
      width: 400px;
    }
    #input_field_brand {
      display: inline;
      width: 170px;
    }
    EOT;
  }

  public function css_by_barcode () {
    $this->css .= <<<EOT
    /* set fixed length for each table column */
    td:nth-child(1) {
      width: 9%;
    }
    td:nth-child(2) {
      width: 30%;
    }
    td:nth-child(3) {
      width: 9%;
    }
    td:nth-child(4) {
      width: 7%;
    }
    td:nth-child(5) {
      width: 8%;
    }
    td:nth-child(6) {
      width: 11%;
    }
    td:nth-child(7) {
      width: 13%;
    }
    td:nth-child(8) {
      width: 13%;
    }
    #input_field_article {
      display: inline;
      width: 400px;
    }
    #input_field_brand {
      display: inline;
      width: 170px;
    }
    EOT;
  }

  public function form_search ($brand = '', $article = '') {
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 700px;">
      <form method="GET">
        <table>
        <tr>
          <td style="width: 30%;">
            <input style="width: 100%;"
            type="search" autofocus="autofocus" onfocus="this.select()"
            id="input_field_brand" name="input_field_brand"
            placeholder="Merke" value="$brand">
          </td>
          <td style="width: 60%;">
            <input style="width: 100%;"
            type="search" id="input_field_article" name="input_field_article"
            placeholder="Artikkel" value="$article">
          </td>
          <td style="width: 10%;">
            <input style="width: 100%;" type="submit" value="Søk" >
          </td>
        </tr>
        </table>
      </form>
    </div><br>\n
    EOT;
  }

  public function form_barcode ($barcode = '') {
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 400px;">
      <form method="GET">
        <table>
        <tr>
          <td style="width: 30%;">
            <input style="width: 100%;"
            type="search" autofocus="autofocus" onfocus="this.select()"
            id="input_field_barcode" name="input_field_barcode"
            placeholder="Strekkode" value="$barcode">
          </td>
          <td style="width: 10%;">
            <input style="width: 100%;" type="submit" value="Skann" >
          </td>
        </tr>
        </table>
      </form>
    </div><br>\n
    EOT;
  }

  public function image_location ($image = 'empty') {
    if ($image == 'empty') {
      return;
    }
    $floor = false;
    $circle = false;

    // grab first letter for the location (example: L-A-30 = L)
    $letter = strtoupper($image[0]);
    foreach ($this->location_index as $index => $value) {
      if ($index == $letter) {
        $floor = $value;
        $circle = $index;
      }
    }
    if (($floor !== false) and ($circle !== false)) {
      // TODO: add check if file exists and fallback to default image if not
      $image_map = $this->image_path_location . "/floor/$floor.png";


      // for items stored in shop, we do not have location as the whole floor serves as one location
      $image_location = $this->image_path_location . "/circle/$circle.png";
      if ( is_numeric($floor) ) {
        $image_location = $this->image_path_location . "/circle/pick_item.png";
      }

      $b64_map = base64_encode(file_get_contents($image_map));
      $b64_circle = base64_encode(file_get_contents($image_location));

      $this->css .= <<<EOT
      #image_map {
          display: block;
          / *margin-left: auto;
          margin-right: auto; */
          width: 50%;
      }
      #image_base {
        position: absolute;
      }

      #image_circle {
        position: relative;
        animation-name: circle_animate;
        animation-duration: 1s;
      }
      @keyframes circle_animate {

        0%  {left:0px; top:-40px;}
        100% {left:0px; top:0px;}
      }
      EOT;

      $this->html .= <<<EOT
      <div id="image_map">
        <img id="image_base"  src="data:image/png;base64,$b64_map" width="700">
        <img id="image_circle" src="data:image/png;base64,$b64_circle" width="700">
      </div>
      EOT;
    }
  }

}
