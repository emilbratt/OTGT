<?php

require_once '../applications/Template.php';

class TemplateReports extends Template {

  protected $arr_convert_sql_to_nor;

  function __construct () {
    parent::__construct();

    $this->arr_convert_sql_to_nor = [
      'YEAR' => 'År tilbake',
      'MONTH' => 'Måneder tilbake',
      'WEEK' => 'Uker tilbake',
      'DAY' => 'Dager tilbake',
    ];

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
      width: 160px;
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

  public function reports_form_input_date ($submit_string = null) {
    $this->css .= <<<EOT
    .reports_form_input_date {
      display: block;
    }
    EOT;
    $str = 'Velg fra dato til dato';
    if ($submit_string !== null) {
      $str = $submit_string;
    }
    // default pre-defined value in the calendar form or from last used e.g. GET
    $_pre_value_from_date = date("Y-m-d");
    $_pre_value_to_date = date("Y-m-d");
    if ( isset($_GET['calendar_from_date']) ) {
      $_pre_value_from_date = $_GET['calendar_from_date'];
    }
    if ( isset($_GET['calendar_to_date']) ) {
      $_pre_value_to_date = $_GET['calendar_to_date'];
    }
    $this->html .= <<<EOT
    <div class="reports_form_input_date">
    <form method="GET">

    <input
      type="hidden"
      name="date_type"
      value="calendar">

    <input
      id="from_date"
      type="date"
      value="$_pre_value_from_date"
      min="2011-01-01"
      name="calendar_from_date">

    <input
      id="to_date"
      type="date"
      value="$_pre_value_to_date"
      min="2011-01-01"
      name="calendar_to_date">

    <input
      style="display: inline-block;"
      type="submit"
      value="Velg fra dato til dato">
    </form>
    </div>
    EOT;
  }

  public function reports_form_brand_year_num_stock_limit () {
   /**
    * this form fetches:
    *   brand name
    *   datepart: years/months/weeks
    *   datepart num: N years/months/weeks back in time
    *   stock operator < or >
    *   N stock limit
    */
    // this logic preserves previous query string and add them to the form
    $brand = '';
    if (isset($_GET['input_field_brand'])) {
      $brand = $_GET['input_field_brand'];
    }
    $date_part_num = '1';
    if (isset($_GET['input_field_date_part_num'])) {
      $date_part_num = $_GET['input_field_date_part_num'];
    }
    $stock_limit = '0';
    if (isset($_GET['input_field_stock_num'])) {
      $stock_limit = $_GET['input_field_stock_num'];
    }
    $location = '';
    if (isset($_GET['input_field_location'])) {
      $location = $_GET['input_field_location'];
    }
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 300px;">
      <form method="GET">
        <table>
        <tr>
          <td colspan="2">
            <input style="width: 100%;"
            type="search" autofocus="autofocus" onfocus="this.select()"
            id="input_field_brand" name="input_field_brand"
            placeholder="Merke" value="$brand">
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <input style="width: 100%;"
            type="search"
            id="input_field_location" name="input_field_location"
            placeholder="Lager" value="$location">
          </td>
        </tr>
        <tr>
          <td style="width: 75%;">
            <select style="width: 100%;" id="input_field_date_part_type" name="input_field_date_part_type">\n
    EOT;
    foreach ($this->arr_convert_sql_to_nor as $eng => $nor) {
      $this->html .= <<<EOT
              <option value="$eng">$nor</option>\n
      EOT;
    }
    $this->html .= <<<EOT
            </select>
          </td>
          <td style="width: 25%;">
            <input style="width: 100%;"
              type="search" id="input_field_date_part_num" name="input_field_date_part_num"
              value="$date_part_num">
          </td>
        </tr>
        <tr>
        <td style="width: 75%;">
          <select style="width: 100%;" id="input_field_stock_operator" name="input_field_stock_operator">\n
            <option value=">">Andtall på lager over</option>
            <option value="<">Andtall på lager under</option>
          </select>
        </td>
          <td style="width: 25%;">
            <input style="width: 100%;"
              type="search" id="input_field_stock_num" name="input_field_stock_num"
              value="$stock_limit">
          </td>
          </tr>
          <tr>
          <td colspan="2" style="width: 100%;">
            <input style="width: 100%;" type="submit" value="Generer Rapport" >
          </td>
        </tr>
        </table>
      </form>
    </div><br>\n
    EOT;
  }

  public function report_form_sales_per_hour () {
    // this logic preserves previous query string and add them to the form
    $db_first_year = 2011;
    $db_current_year = intval(date("Y"));
    $year = $db_current_year;
    if (isset($_GET['input_field_YYYY'])) {
      $year = $_GET['input_field_YYYY'];
    }
    $month = '';
    if (isset($_GET['input_field_MM'])) {
      $month = $_GET['input_field_MM'];
    }
    $dom = '';
    if (isset($_GET['input_field_DOM'])) {
      $dom = $_GET['input_field_DOM'];
    }
    $dow = '';
    if (isset($_GET['input_field_DOW'])) {
      $dow = $_GET['input_field_DOW'];
    }
    $hod = '';
    if (isset($_GET['input_field_HOD'])) {
      $hod = $_GET['input_field_HOD'];
    }
    $this->html .= <<<EOT
    <div id="input_field_div" style="width: 600px;">
      <form method="GET">
        <table>
        <tr>
          <td>År</td>
          <td>Måned</td>
          <td>Dato</td>
          <td>Ukedag</td>
          <td>Klokketime</td>
        </tr>
        <tr>
          <td style="width: 30%;">
          <select style="width: 100%;" id="input_field_YYYY" name="input_field_YYYY">\n
    EOT;
    while ($db_current_year >= $db_first_year) {
      if ( $db_current_year === intval($year) ) {
        $this->html .= <<<EOT
              <option selected value="$db_current_year">$db_current_year</option>\n
        EOT;
      } else {
        $this->html .= <<<EOT
              <option value="$db_current_year">$db_current_year</option>\n
        EOT;
      }
      $db_current_year--;
    }
    $this->html .= <<<EOT
          </select>
          </td>
          <td style="width: 20%;">
            <input style="width: 100%;"
            type="search"
            id="input_field_MM" name="input_field_MM"
            placeholder="1-12" value="$month">
          </td>
          <td style="width: 20%;">
            <input style="width: 100%;"
            type="search"
            id="input_field_DOM" name="input_field_DOM"
            placeholder="1-31" value="$dom">
          </td>
          <td style="width: 20%;">
            <input style="width: 100%;"
            type="search"
            id="input_field_DOW" name="input_field_DOW"
            placeholder="1-7" value="$dow">
          </td>
          <td style="width: 20%;">
            <input style="width: 100%;"
            type="search"
            id="input_field_HOD" name="input_field_HOD"
            placeholder="0-23" value="$hod">
          </td>
          <td style="width: 30%;">
            <input style="width: 100%;" type="submit" value="Generer Rapport" >
          </td>
        </tr>
        </table>
      </form>
    </div><br>\n
    EOT;
  }

  public function message ($str) {
    foreach ($this->arr_convert_sql_to_nor as $eng => $nor) {
      str_replace($eng, $nor, $str);
    }
    $this->html .= <<<EOT
    <div class="message">
      <p><i>$str</i></p>
    </div>\n
    EOT;
  }

  public function embed_spreadsheet ($url) {
    // shows an html object window of a pdf where $url is the the pdf target
    // where a body is returned as application/pdf and not html
    $this->html .= <<<EOT
    <object width="100%" height="500" type="text/csv" data="$url">
      <p>Kunne ikke laste inn csv</p>
    </object>\n
    EOT;
  }
}
