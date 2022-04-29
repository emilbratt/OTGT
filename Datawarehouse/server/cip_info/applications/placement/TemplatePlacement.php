<?php

require_once '../applications/Template.php';

class TemplatePlacement extends Template {

  function __construct () {
    parent::__construct();
    $this->css .= <<<EOT
    /* TABLE */
    table {
      font-family: arial;
      border-collapse: collapse;
    }
    td {
      border: 1px solid #202020;
      text-align: center;
      padding-left: 12px;
      padding-right: 12px;
    }
    th {
      background-color: $this->colour_header_background;
      height: 32px;
    }
    #th_no_hyperlink {
      border: 1px solid $this->colour_default_text;
    }\n
    EOT;
  }

  public function _form_scan_item () {
    $this->html .= <<<EOT
    <td>
      <input
         type="text"
         autofocus="autofocus"
         onfocus="this.select()"
         id="form_input_text"
         name="barcode">
    </td>\n
    EOT;
  }

  public function _form_scan_shelf ($article_id, $article = '', $brand = '') {
    // we need article_id to register placement
    // we need article_name and brand_name for showing what sas registered
    $ean = $_POST['barcode'];
    $this->html .= <<<EOT
    <td>
      <input
         type="search"
         autofocus="autofocus"
         onfocus="this.select()"
         id="form_input_text"
         name="shelf">

      <input
        type="hidden"
        name="barcode"
        value="$ean">

      <input
        type="hidden"
        name="article_id"
        value="$article_id">

      <input
        type="hidden"
        name="article"
        value="$article">

      <input
        type="hidden"
        name="brand"
        value="$brand">
    </td>\n
    EOT;
  }

  public function _form_end ($val = 'Enter') {
    $this->html .= <<<EOT
    </tr>
    </table>
    </form>
    </div>\n
    EOT;
  }

  public function placement_get_result () {

  }

}
