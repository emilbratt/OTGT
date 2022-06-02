<?php

require_once '../applications/Template.php';

class TemplateHome extends Template {

  function __construct () {
    parent::__construct();

    $this->css .= <<<EOT
    .note_input_form {
      background-color: $this->colour_search_background;
      color: #BBBBFF;
    }

    #busy_colour_gradient {
      height: 5px;
      background-color: #C4EFFF; /* For browsers that do not support gradients */
      background-image: linear-gradient(
         to right,
         #C4EFFF,
         #A2F2DD,
         #ABF5CC,
         #9BF2B4,
         #96FA99,
         #ADFF85,
         #DEFF7A,
         #FF7C17,
         #FF4B0A,
         #ED0000
       );
    }

    /* TITLE */
    .second_title {
      padding: 0px;
      margin-top: 0px;
      margin-bottom: -15px;
      font-size: 20px;
    }
    /* TABLE */
    table {
      font-family: arial;

      border: none;
    }
    td {
      border: 1px solid #202020;
      text-align: left;
      padding-left: 2px;
      font-size: 18px;
    }
    th {

      height: 32px;
      font-size: 20px;
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
    a button:hover {
      background-color: $this->colour_default_hover;
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
    }\n
    EOT;
  }

  public function second_title ($string) {
    $this->html .= <<<EOT
    <div class="second_title">
      <h3>$string</h3>
    </div>\n
    EOT;
  }

  public function _table_row_value ($string, $text_align = 'center', $font_size = '18', $hyperlink = null) {
    // passing a url as second arg will make it a clickabel button
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

  public function note_input_form ($note = '') {
    $this->html .= <<<EOT
    <div class="">
    <form action="" method="post">
    <!--
      <textarea id="note_input_form" style="font-size: 18px; width:650px; height: 220px;"
    -->
    <textarea id="note_input_form" style="font-size: 18px;"
      name="note_input_form"
      onkeypress="stop_auto_fetch_note()"
      rows="10"
      cols="55"
      class="note_input_form">$note</textarea>
    <input type="submit" value="Lagre Notat">
    </form>
    </div>
    EOT;

    // auto fetch new note, but disable if "on key press event -> stop_auto_fetch_note()"
    $host = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->script .= <<<EOT
    <script>
    function auto_fetch_note() {
      fetch('$host/api/cache/v0/read/home_page_note')
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Could not reach api endpoint.");
        }
      })
      .then(json => document.getElementById("note_input_form").value = json.mem_val)
      .catch(err => console.error(err));
    }

    function stop_auto_fetch_note() {
      clearInterval(auto_fetch_interval_notes);
    }

    // interval is set in millieseconds
    const auto_fetch_interval_notes = setInterval(auto_fetch_note, 10000);
    </script>
    EOT;

  }

  public function shop_how_busy ($seed_minutes = '5') {
    $this->html .= <<<EOT

    <div style="width: 20%;">
      <div id="shop_busy_banner_desc" style="width:100%; text-align: left; font-size: 18px;">
        Henter butikkstatus..
      </div>

      <div id="busy_colour_gradient"></div>

      <div id="shop_busy_arrow" style="width:0%; background-color: $this->colour_page_background; text-align: right; font-size: 28px;"></div>
    </div>\n
    EOT;

    // auto fetch new note, but disable if "on key press event -> stop_auto_fetch_note()"
    $host = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->script .= <<<EOT
    <script>
    function auto_fetch_shop_busy() {
      fetch('$host/api/shop/v0/howbusy/$seed_minutes')
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Could not reach api endpoint.");
        }
      })
      .then((json) => {
        document.getElementById("shop_busy_banner_desc").innerHTML = json['desc'];
        document.getElementById("shop_busy_arrow").style.width = json['precent'];
        document.getElementById("shop_busy_arrow").innerHTML = '&#x2191';
      })
      .catch(err => console.error(err));
    }


    // interval is set in millieseconds
    const auto_fetch_interval_shop_busy = setInterval(auto_fetch_shop_busy, 2000);
    </script>
    EOT;

  }


}
