<?php

require_once '../applications/Template.php';

class TemplatePlacement extends Template {

  function __construct () {
    parent::__construct();
  }


  public function _form_scan_item () {
    $this->html .= <<<EOT
    <td>
      <input
         type="text"
         autofocus="autofocus"
         onfocus="this.select()"
         id="form_input_text"
         name="placement_scan_item">
    </td>\n
    EOT;
  }

  public function _form_scan_shelf ($barcode) {
    // $ref = what key to reference in GET / POST array
    // article id for previous scanned value that is passed along the form
    $this->html .= <<<EOT
    <td>
      <input
         type="search"
         autofocus="autofocus"
         onfocus="this.select()"
         id="form_input_text"
         name="placement_scan_shelf">

      <input
        type="hidden"
        name="placement_scan_item"
        value="$barcode">
    </td>\n
    EOT;
  }

  public function form_end ($val = 'Enter') {
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
