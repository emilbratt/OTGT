<?php

require_once '../applications/Template.php';

class TemplateInstructions extends Template {

  function __construct () {
    parent::__construct();
    $this->css .= <<<EOT
    button, select {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      height: 30px;
    }
    button {
      width: 250px;
    }
    select {
      width: 170px;
    }
    button:hover, select:hover {
      background-color: $this->colour_default_hover;
    }
    input[type="file"] {
      display: none;
    }
    .custom_file_upload_button {
      background-color: $this->colour_input_background;
      color: $this->colour_default_text;
      border: 1px solid $this->colour_default_border;
      display: inline-block;
      padding: 5px 10px;
    }
    .custom_file_upload_button:hover {
      background-color: $this->colour_default_hover;
    }
    /* hide the qr code and show when clicking button */
    #image_show {
      display: none;
    }
    .image_show {
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    /* TABLE */
    table {
      font-family: arial;
      font-size: 18px;
    }
    td {
      border: 1px solid $this->colour_default_border;
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
    tr {

      border: 1px solid $this->colour_default_border;
    }

    \n
    EOT;
  }

  public function form_add_instruction_category () {
    $this->html .= <<<'EOT'
    <form method="POST">
    <input
      type="text"
      name="input_field_instructions_add_category"
      placeholder="Ny Kategori">
    <input
      type="submit"
      name="input_field_instructions_add_category_submit"
      value="Legg Til" />
    </form>
    EOT;
  }

  public function form_upload_instruction ( $categories = array() ) {
    if ( empty($categories)) {
      return;
    }
    $this->html .= <<<EOT
    <form enctype="multipart/form-data" method="POST">
      <select id="input_field_instructions_select_category"
        name="input_field_instructions_select_category">\n
    EOT;
    foreach ($categories as $category) {
      $show = str_replace('_', ' ', $category);
      $this->html .= <<<EOT
        <option value="$category">$show</option>\n
      EOT;
    }
    $this->html .= <<<'EOT'
      </select>

      <label for="button_file_upload" class="custom_file_upload_button">Velg Fil</label>
      <!-- 10 MB = 1024 * (1024 * 10) = 10485760 bytes -->
      <input
        type="hidden"
        name="MAX_FILE_SIZE"
        value="10485760" />

      <input required
        type="file"
        id="button_file_upload"
        name="input_field_instructions_upload_file" />

      <input
        type="submit"
        name="input_field_instructions_upload_submit"
        value="Last opp" />
    </form>
    EOT;
  }

  public function form_delete_instruction_category ( $categories = array() ) {
    if ( empty($categories)) {
      return;
    }
    $this->html .= <<<EOT
    <form method="POST">
      <select id="input_field_instructions_delete_category"
        name="input_field_instructions_delete_category">\n
    EOT;
    foreach ($categories as $category) {
      $show = str_replace('_', ' ', $category);
      $this->html .= <<<EOT
        <option value="$category">$show</option>\n
      EOT;
    }
    $this->html .= <<<'EOT'
      </select>
      <input
        type="submit"
        name="input_field_instructions_upload_submit"
        value="Slett Kategori" />
    </form>
    EOT;
  }

  public function button_show_qr_code () {
    $this->html .= <<<EOT
    <button onclick="show_qr_code()">QR-kode</button>\n
    EOT;
    $this->script .= <<<EOT
    <script>
    function show_qr_code() {
      var x = document.getElementById("image_show");
      x.style.display = "block";
    }
    </script>\n
    EOT;
  }

  public function button_fetch_api_delete_instruction ($category = '', $instruction = '') {
    // this button sends request to api and the api handles validation etc.
    $host = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->html .= <<<EOT
    <button id="button_fetch_api_delete_instruction">Slett Instruks</button>\n
    EOT;
    $this->script .= <<<EOT
    <script>
    function button_fetch_api_delete_instruction() {
      fetch('$host/api/instructions/v0/delete/$category/$instruction', {
        method: 'DELETE'
      }).then(response => {
        if (response.ok) {
          document.getElementById('button_fetch_api_delete_instruction').style.backgroundColor = '$this->colour_update_value_ok';
          alert("Instruks er slettet");
        } else {
          document.getElementById('button_fetch_api_delete_instruction').style.backgroundColor = '$this->colour_update_value_error';
          alert("Instruks Kunne ikke slettes");
        }
      });

    }
    let btn = document.getElementById("button_fetch_api_delete_instruction");
    btn.addEventListener('click', event => {
      button_fetch_api_delete_instruction();
    });
    </script>\n
    EOT;
  }

  public function embed_pdf ($url) {
    // shows an html object window of a pdf where $url is the the pdf target
    // where a body is returned as application/pdf and not html
    $this->html .= <<<EOT
    <object width="100%" height="500" type="application/pdf" data="$url">
      <p>Kunne ikke laste inn pdf</p>
    </object>\n
    EOT;
  }

  public function image_show ($image) {
    $b64image = base64_encode($image);
    $this->html .= <<<EOT
    <div id="image_show">
      <img class="image_show" src="data:image/png;base64,$b64image">
    </div>\n
    EOT;
  }

}
