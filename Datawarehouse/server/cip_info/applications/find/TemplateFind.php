<?php

require_once '../applications/Template.php';

class TemplateFind extends Template {
  // methods with same name here will override the method in Template

  function __construct () {
    parent::__construct();
    $this->html .= <<<EOT
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

  public function script_filter_row () {
    $this->html .= <<<EOT
    <script>
    function filter_row() {
      var input, filter, table, tr, td, i, text_val;
      input = document.getElementById("filter_row");
      filter = input.value.toUpperCase();
      table = document.getElementById("find_item");
      tr = table.getElementsByTagName("tr");
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
          text_val = td.textContent || td.innerText;
          if (text_val.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
      }
    }
    </script>\n
    EOT;
  }

  public function form_search ($brand = '', $article = '') {
    $this->html .= <<<EOT
    <div id="input_field_div">
      <form>
        <!-- <label for="input_field_brand"><h3 class="inline">Merke:</h3></label> -->
        <input
          type="search" autofocus="autofocus" onfocus="this.select()"
          id="input_field_brand" name="input_field_brand"
          placeholder="Merke" value="$brand">

        <!-- <label for="input_field_article"><h3 class="inline">Artikkel:</h3></label> -->
        <input
          type="search" id="input_field_article" name="input_field_article"
          placeholder="Artikkel" value="$article">

        <input type="submit" value="Søk" id="hidden_submit">

      </form>
    </div><br>\n
    EOT;
  }

  public function table_row_header_filter () {
    $this->html .= <<<EOT
    <th>
      <input style="width: 100%;" type="text" id="filter_row" onkeyup="filter_row()" placeholder="Filtrer" title="Type in a name">
    </th>\n
    EOT;
  }

  public function table_start () {
    $this->html .= <<<EOT
    <table id="find_item">
    EOT;
  }

  public function table_row_start () {
    $this->html .= <<<EOT
    <tr>\n
    EOT;
  }

  public function table_row_value ($string) {
    $this->html .= <<<EOT
    <td>$string</td>\n
    EOT;
  }

}
