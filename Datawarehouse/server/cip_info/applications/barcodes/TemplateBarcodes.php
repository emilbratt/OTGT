<?php

require_once '../applications/Template.php';

class TemplateBarcodes extends Template {

  function __construct () {
    parent::__construct();

    $this->css .= <<<EOT
    .short_input_length {
      width: 80px;
    }
    #medium_input_length {
      width: 150px
    }
    #form_input_label {
      width: 400px
    }
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
    /* show image from bytestream */
    .image_show {
      display: block;
      margin-left: auto;
      margin-right: auto;
    }\n
    EOT;
  }

  public function _barcode_form ($sheet_limit, $char_limit) {
    // the sheet_limit must be passed because we need to know the maximum
    // number of input fields -> shelf labels that can fit on a paper sheet
    $this->html .= <<<EOT
    <div class="center_div">
    <form enctype="multipart/form-data" method="POST">\n
    EOT;
    for ($i = 1; $i <= $sheet_limit; $i+=2) {
      $odd = strval($i);
      $even = strval($i + 1);
      $this->html .= <<<EOT
      <div>
        <input id="short_input_length" type="text" name="$odd" maxlength="$char_limit">
        <input id="short_input_length" type="text" name="$even" maxlength="$char_limit">
      </div>\n
      EOT;
    }
    $this->html .= <<<EOT
    <input id="medium_input_length" type="submit" value="Generer">
    </form>
    </div>\n
    EOT;
  }

  public function _shelf_label_form ($sheet_limit, $char_limit) {
    // the sheet_limit must be passed because we need to know the maximum
    // number of input fields -> shelf labels that can fit on a paper sheet
    $this->html .= <<<EOT
    <div class="center_div">
    <form enctype="multipart/form-data" method="POST">\n
    EOT;
    for ($i = 1; $i <= $sheet_limit; $i+=2) {
      $odd = strval($i);
      $even = strval($i + 1);
      $this->html .= <<<EOT
      <div>
        <input
          id="input_id_$odd"
          class="short_input_length"
          type="text"
          name="$odd"
          onkeyup="sanitize_input_for_shelf_label('$odd')"
          maxlength="$char_limit">

        <input
          id="input_id_$even"
          class="short_input_length"
          type="text"
          name="$even"
          onkeyup="sanitize_input_for_shelf_label('$even')"
          maxlength="$char_limit">

      </div>\n
      EOT;
    }
    $this->html .= <<<EOT
    <input id="medium_input_length" type="submit" value="Generer">
    </form>
    </div>\n
    EOT;

    $this->script .= <<<EOT
    <script>
    // force all input to upper case and whitespace to underscore
    function sanitize_input_for_shelf_label(N) {
      var x = document.getElementById('input_id_' + N);
      x.value = x.value.toUpperCase();
      x.value = x.value.replace(/\s+/g, '-');
    }
    </script>\n
    EOT;
  }

}
