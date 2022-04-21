<?php

/**
 *
 * TODO:
 *  nothing at the moment
 *
 */

require_once '../applications/Template.php';

class TemplateAPI extends Template {

  function __construct () {
    parent::__construct();

    $method_colour_get = '#555577';
    $method_colour_post = '#557755';
    $method_colour_delete = '#775555';
    $method_colour_put = '#775577';
    $this->css .= <<<EOT
    #endpoint_title {
      font-size: 22px;
      margin-bottom: 2px;
    }
    #GET {
      background-color: $method_colour_get;
      text-align: center;
    }
    #POST {
      background-color: $method_colour_post;
      text-align: center;
    }
    #DELETE {
      background-color: $method_colour_delete;
      text-align: center;
    }
    #PUT {
      background-color: $method_colour_put;
      text-align: center;
    }
    th {
      background-color: $this->colour_header_background;

      text-align: center;
      font-size: 22px;
      padding: 2px 2px;
    }
    th a {
      height: 27px;
      font-size: 20px;
    }
    td {
      background-color: $this->colour_header_background;
      text-align: left;
      padding: 1px 10px;
      font-size: 18px;
    }
    /* set fixed length for each table column */
    td:nth-child(1) {
      width: 80px;
    }
    td:nth-child(2) {
      width: 800px;
    }
    td:nth-child(3) {
      width: 700px;
    }\n
    EOT;
  }

  public function endpoint_title ($str) {
    $this->html .= <<<EOT
    <p id="endpoint_title">$str</p>\n
    EOT;
  }

  public function table_row_value ($string, $hyperlink = null) {
    // passing a url as second arg will make it a clickabel button

    // if the string has an htttp method, we use this as html object id for css
    if ($hyperlink == null) {
      $this->html .= <<<EOT
          <td id="$string">$string</td>\n
      EOT;
      return;
    }
    $this->html .= <<<EOT
        <td id="$string"><a href="$hyperlink">$string</a></td>\n
    EOT;
  }

}
