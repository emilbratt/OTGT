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

  public function css_result_set () {
    $this->css .= <<<EOT
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
    th a {
      height: 27px;
      font-size: 20px;
    }
    tr:nth-child(even) {
      background-color: $this->colour_row_background_2;
    }
    tr:nth-child(odd) {
      background-color: $this->colour_row_background_1;
    }

    #hidden_submit {
      display: none;
    }
    #input_field_div {
      display: block;
    }
    #search_field {
      background-color: $this->colour_search_background;
      display: inline-block;
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

    #table_td_label {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
    }
    select {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      width: 150px;
      height: $this->form_default_height;
    }
    /* set fixed length for each table column */
    td:nth-child(1) {
      width: 10%;
    }
    td:nth-child(2) {
      width: 57%;
    }
    td:nth-child(3) {
      width: 7%;
    }
    td:nth-child(4) {
      width: 8%;
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
    }\n
    EOT;
  }

  public function css_by_barcode () {
    $this->css .= <<<EOT
    /* set fixed length for first table column */
    td:nth-child(1) {
      width: 150px;
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

  public function form_search () {
    $article = '';
    if ( isset($_GET['input_field_article'])) {
      $article = $_GET['input_field_article'];
    }
    $brand = '';
    if ( isset($_GET['input_field_brand'])) {
      $brand = $_GET['input_field_brand'];
    }
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

  public function form_barcode ($action = "byarticle") {
    // $action will send to specified app
    $barcode = '';
    if ( isset($_GET['input_field_barcode']) ) {
      $barcode = $_GET['input_field_barcode'];
    }
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 400px;">
      <form method="GET" action="$action">
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


  public function form_shelf () {
    $shelf = '';
    if ( isset($_GET['input_field_shelf'])) {
      $shelf = $_GET['input_field_shelf'];
    }
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 700px;">
      <form method="GET">
        <table>
        <tr>
          <td style="width: 60%;">
            <input style="width: 100%;"
            type="search"  autofocus="autofocus" onfocus="this.select()"
            id="input_field_article" name="input_field_article"
            placeholder="Plassering X-X-Y" value="$shelf">
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

  public function title ($string = 'title') {
    $this->html .= <<<EOT
    <div class="title">
      <h3 style="margin-bottom: 2px;">$string</h3>
    </div>\n
    EOT;
  }

  public function _table_row_value ($string, $text_align = 'center', $font_size = '18', $hyperlink = null) {
    // passing a url as second arg will make the cell clickable
    $font_size = $font_size . 'px';
    if ($hyperlink == null) {
      $this->html .= <<<EOT
          <td style="font-size: $font_size; text-align: $text_align;">$string</td>\n
      EOT;
      return;
    }
    $this->html .= <<<EOT
        <td style="font-size: $font_size; text-align: $text_align;">
          <a href="$hyperlink">
            <button style="width: 100%; font-size: 20px;" id="input_field_submit">$string</button>
          </a>
        </td>\n
    EOT;
  }

}
