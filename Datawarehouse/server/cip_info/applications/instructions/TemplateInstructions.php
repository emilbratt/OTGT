<?php

require_once '../applications/Template.php';

class TemplateInstructions extends Template {

  function __construct () {
    parent::__construct();
    $this->css .= <<<EOT
    button {
      border: 1px solid $this->colour_default_text;
      display: inline;
      font-size: 15px;
      color: $this->colour_default_text;
      background-color: $this->colour_default_background;
      width: 170px;
      height: 30px;
    }
    button:hover {
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
    }\n
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
    <p>Velg Kategori:</p>
    <form enctype="multipart/form-data" method="POST">
      <select id="input_field_instructions_select_category"
        name="input_field_instructions_select_category">\n
    EOT;
    foreach ($categories as $category) {
      $this->html .= <<<EOT
        <option value="$category">$category</option>\n
      EOT;
    }
    $this->html .= <<<'EOT'
      </select>
      <p>Velg Fil:</p>
      <!-- 10 MB = 1024 * (1024 * 10) = 10485760 bytes -->
      <input
        type="hidden"
        name="MAX_FILE_SIZE"
        value="10485760" />

      <input required
        type="file"
        name="input_field_instructions_upload_file" />
      <br>

      <input
        type="submit"
        name="input_field_instructions_upload_submit"
        value="Last opp" />
    </form>
    <br>
    EOT;
  }

  public function form_delete_instruction_category ( $categories = array() ) {
    if ( empty($categories)) {
      return;
    }
    $this->html .= <<<EOT
    <form method="POST">
      <label for="input_field_instructions_delete_category">
        Velg Kategori:
      </label>
      <select id="input_field_instructions_delete_category"
        name="input_field_instructions_delete_category">\n
    EOT;
    foreach ($categories as $category) {
      $this->html .= <<<EOT
        <option value="$category">$category</option>\n
      EOT;
    }
    $this->html .= <<<'EOT'
      </select><br>
      <input
        type="submit"
        name="input_field_instructions_upload_submit"
        value="Slett Kategori" />
    </form><br>
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
    <object width="100%" height="800" type="application/pdf" data="$url">
      <p>Kunne ikke laste inn pdf</p>
    </object>\n
    EOT;
  }


}
