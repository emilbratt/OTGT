<?php

require_once '../applications/Template.php';

class TemplateFind extends Template {
  // methods with same name here will override the method in Template

  function __construct () {
    parent::__construct();
  }

  public function form_search ($brand = '', $article = '') {
    $this->html .= <<<EOT
    <div id="input_field_div">
      <form>
        <label for="input_field_brand"><h3 class="inline">Merke:</h3></label>
        <input
          type="search" autofocus="autofocus" onfocus="this.select()"
          id="input_field_brand" name="input_field_brand"
          value="$brand">

        <label for="input_field_article"><h3 class="inline">Artikkel:</h3></label>
        <input
          type="search" id="input_field_article" name="input_field_article"
          value="$article">

        <input type="submit" value="Søk" id="input_field_submit">

      </form>
    </div>
    <br><br>\n
    EOT;
  }

}
