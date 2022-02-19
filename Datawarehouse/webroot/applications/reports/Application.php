<?php

/*
notes:
for turnover reports, maybe include graphs using some graphing tool for web view

// example request: http://host:port/reports/soldout/&type=thismonth&include=none-defaults&filter=default&sort=brand&order=accendings

*/

class Home {
  function __construct () {

    $reports = [
      'Utsolgt idag' => '/reports/soldout/today',
      'Utsolgt denne uken' => '/reports/soldout/week',
    ];
    foreach ($reports as $name => $page) {
      echo '<a href="http://'.$_SERVER['HTTP_HOST'].$page.'">'.$name.'</a><br>';
    }
  }
}


// TO BE REMOVED
// class Soldout {
//   function __construct () {
//     $page = Pagerequest::get_file('./applications/reports/soldout');
//     if($page !== false) {
//       require_once $page;
//       $page = new Page();
//     }
//   }
// }

class Soldout {
  function __construct () {
    require_once './applications/Database.php';
    require_once './applications/Helpers.php';
    require_once './applications/reports/html_template.php';
    require_once './applications/reports/QueryReports.php';

    $query = QuerySoldout::get();
    $this->cnxn = Database::get_connection();

    // $this->query = $this->get_query_exlude_common();


    // load html doc type, css style and body start tag
    echo Template::doc_head();
    echo Template::doc_style();
    echo Template::doc_start();
    echo Template::doc_title_left('Rapport: Utsolgte varer i ???');
    echo Template::doc_title_right('Dato: ' . Dates::get_weekday() . ' '. date("d/m-Y"));

    echo '<table>';
    echo '<tr>';
    echo ' <th>Merke</th>';
    echo ' <th>Navn</th>';
    echo ' <th>Antall</th>';
    echo ' <th>Plasserng</th>';
    echo ' <th>Sist_Importert</th>';
    echo ' <th>Lev_id</th>';
    echo '</tr>';
    foreach ($this->cnxn->query($query) as $row) {
      echo '<tr>';
      $brand = CharacterConvert::utf_to_norwegian($row['Merke']);
      $name = CharacterConvert::utf_to_norwegian($row['Navn']);
      $qty = CharacterConvert::utf_to_norwegian($row['Antall']);
      $location = CharacterConvert::utf_to_norwegian($row['Plasserng']);
      $last_import = CharacterConvert::utf_to_norwegian($row['Sist_Importert']);
      $supply_id = CharacterConvert::utf_to_norwegian($row['Lev_id']);
      echo "<td>$brand</td>";
      echo "<td>$name</td>";
      echo "<td>$qty</td>";
      echo "<td>$location</td>";
      echo "<td>$last_import</td>";
      echo "<td>$supply_id</td>";
    }
    echo '</tr>';
    echo '</table>';

    // close remaining html tags
    echo Template::doc_end();
  }
}





class Turnover {
  function __construct () {
    echo 'this is reports - Turnover served from Application.php';
  }
}
