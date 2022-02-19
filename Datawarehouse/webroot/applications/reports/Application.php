<?php

/*
notes:
for turnover reports, maybe include graphs using some graphing tool for web view

// example request: http://host:port/reports/soldout/&type=thismonth&include=none-defaults&filter=default&sort=brand&order=accendings

*/

class Home {
  function __construct () {
    // links to the reports listed as classes below
    echo Template::doc_start();
    $reports = [
      'Utsolgt idag' => '/reports/soldout&type=thisday',
      'Utsolgt denne uken' => '/reports/soldout&type=thisweek',
    ];
    foreach ($reports as $name => $page) {
      echo '<a href="http://'.$_SERVER['HTTP_HOST'].$page.'">'.$name.'</a><br>';
    }
  }
}


class Soldout {
  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once './applications/Database.php';
    require_once './applications/Helpers.php';
    require_once './applications/reports/Template.php';
    require_once './applications/reports/QueryReports.php';

    $type = 'today';
    $left_title = 'Rapport: Utsolgte varer i dag';
    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'today':
        $left_title = 'Rapport: Utsolgte varer i dag';
        break;
      case 'thisweek':
        $left_title = 'Rapport: Utsolgte varer denne uken';
      break;
      case 'thismonth':
        $left_title = 'Rapport: Utsolgte varer '. Dates::get_this_month() . ' ' . date("Y");
      break;
    }
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");
    $table_headers = [
      'Merke', 'Navn', 'Antall', 'Plassering', 'Sist Importert', 'Lev. ID',
    ];

    // html starts here
    $template = new Template();
    $template->start();
    $template->title_left($left_title);
    $template->title_right($right_title);

    // report table starts here
    $template->table_start();
    $template->table_row_start();
    foreach ($table_headers as $header) {
      $template->table_header_value($header);
    }
    $template->table_row_end();
    $query = QuerySoldout::get($type);
    $this->cnxn = Database::get_connection();
    foreach ($this->cnxn->query($query) as $row) {
      $template->table_row_start();
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['last_imported']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['supply_id']));
      $template->table_row_end();
    }
    $template->table_end();

    // html ends here
    $template->end();

    // prints out the whole template that is generated
    $template->print();
  }
}





class Imported {
  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once './applications/Database.php';
    require_once './applications/Helpers.php';
    require_once './applications/reports/Template.php';
    require_once './applications/reports/QueryReports.php';

    $type = 'today';
    $left_title = 'Rapport: Utsolgte varer i dag';
    if(isset($_GET['type'])) {
      $type = $_GET['type'];
    }
    switch ($type) {
      case 'today':
        $left_title = 'Rapport: Utsolgte varer i dag';
        break;
      case 'thisweek':
        $left_title = 'Rapport: Utsolgte varer denne uken';
      break;
      case 'thismonth':
        $left_title = 'Rapport: Utsolgte varer '. Dates::get_this_month() . ' ' . date("Y");
      break;
    }
    $right_title = 'Dato idag: ' . Dates::get_this_weekday() . ' '. date("d/m-Y");
    $table_headers = [
      'Merke', 'Navn', 'Importert', 'Lager', 'Plassering', 'Lev. ID', 'Sist Importert', '',
    ];

    // html starts here
    $template = new Template();
    $template->start();
    $template->title_left($left_title);
    $template->title_right($right_title);

    // report table starts here
    $template->table_start();
    $template->table_row_start();
    foreach ($table_headers as $header) {
      $template->table_header_value($header);
    }
    $template->table_row_end();
    $query = QueryImported::get($type);
    $this->cnxn = Database::get_connection();
    foreach ($this->cnxn->query($query) as $row) {
      $template->table_row_start();
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['brand']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['article']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['import_qty']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['quantity']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['location']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['supply_id']));
      $template->table_row_value(CharacterConvert::utf_to_norwegian($row['last_imported']));
      $template->table_row_end();
    }
    $template->table_end();

    // html ends here
    $template->end();

    // prints out the whole template that is generated
    $template->print();
  }
}
