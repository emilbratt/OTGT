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

  function __construct () {
    parent::__construct();
    $this->image_path_location = $this->image_path . '/location';
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
          <td style="width: 60%;">
            <input style="width: 100%;"
            type="search"  autofocus="autofocus" onfocus="this.select()"
            id="input_field_article" name="input_field_article"
            placeholder="Artikkel" value="$article">
          </td>
          <td style="width: 30%;">
            <input style="width: 100%;"
            type="search"
            id="input_field_brand" name="input_field_brand"
            placeholder="Merke" value="$brand">
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

}
