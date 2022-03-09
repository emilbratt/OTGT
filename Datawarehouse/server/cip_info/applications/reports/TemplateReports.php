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
  }

  public function reports_form_input_date () {
    $this->css .= <<<EOT
    .reports_form_input_date {
      display: block;
    }
    EOT;
    $_date = date("Y-m-d");
    $this->html .= <<<EOT
    <div class="reports_form_input_date">
    <form method="GET">
    <input
      type="date"
      value="$_date"
      min="2011-01-01"
      name="type">

    <input
      type="submit"
      value="Velg Dato" >
    </form>
    </div>
    EOT;
  }

  public function reports_form_brand_year_num_stock_limit ($brand = '', $date_part_num = '1', $stock_limit = '0') {
    // this form fetches:
    // brand name
    // datepart: years/months/weeks
    // datepart num: N years/months/weeks back in time
    // stock operator < or >
    // N stock limit

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

}
