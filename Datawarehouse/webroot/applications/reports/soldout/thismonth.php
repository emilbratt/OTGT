<?php

// URL: http://host:port/reports/soldout/today

class Page {

  private $query;
  private $cnxn;

  function __construct () {
    require_once './applications/reports/soldout/html_template.php';
    require_once './applications/Database.php';
    require_once './applications/Helpers.php';
    $this->cnxn = Database::get_connection();
    $this->query = $this->get_query_exlude_common();

    // if GET array is issued
    if(isset($_GET['include'])) {
      if($_GET['include'] == 'all') {
        $this->query = $this->get_query_include_common();
      }
    }
    if(isset($_GET['sort'])) {
      if($_GET['sort'] == 'brand') {
        $this->query = $this->get_query_exlude_common_sort_brand();
      }
    }

    // load html doc type, css style and body start tag
    echo Template::doc_head();
    echo Template::doc_style();
    echo Template::doc_start();
    echo Template::doc_title_left('Rapport: Utsolgte varer denne måneden');
    echo Template::doc_title_right('Dato: ' . Dates::get_weekday() . ' '. date("d/m-Y"));

    echo '<table style="width:100%">';
    echo '<tr>';
    echo ' <th>Merke</th>';
    echo ' <th>Navn</th>';
    echo ' <th>Dato</th>';
    echo ' <th>Antall</th>';
    echo ' <th>Plasserng</th>';
    echo ' <th>Sist_Importert</th>';
    echo ' <th>Lev_id</th>';
    echo '</tr>';
    foreach ($this->cnxn->query($this->query) as $row) {
      echo '<tr>';
      $brand = CharacterConvert::utf_to_norwegian($row['Merke']);
      $name = CharacterConvert::utf_to_norwegian($row['Navn']);
      $day = CharacterConvert::utf_to_norwegian($row['Dato']);
      $qty = CharacterConvert::utf_to_norwegian($row['Antall']);
      $location = CharacterConvert::utf_to_norwegian($row['Plasserng']);
      $last_import = CharacterConvert::utf_to_norwegian($row['Sist_Importert']);
      $supply_id = CharacterConvert::utf_to_norwegian($row['Lev_id']);
      echo "<td>$brand</td>";
      echo "<td>$name</td>";
      echo "<td>$day</td>";
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


  private function get_query_exlude_common () {
    return <<<EOT
    SET LANGUAGE NORWEGIAN
    SELECT
      Brands.brandLabel AS Merke,
      Article.articleName AS Navn,
      DAY(articleStock.lastSold) AS Dato,
      CAST (stockQty AS INT) AS Antall,
      articleStock.StorageShelf AS Plasserng,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS Sist_Importert,
      Article.suppliers_art_no AS Lev_id

    FROM
      Article
      INNER JOIN articleStock ON Article.articleId = articleStock.articleId
      INNER JOIN Brands ON Article.brandId = Brands.brandId

    WHERE
      DATEPART(MONTH, articleStock.lastSold) = DATEPART(MONTH, CURRENT_TIMESTAMP) AND
      DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP) AND
      ArticleStatus = '0' AND Article.articleName NOT LIKE '[.]%' AND stockQty<='0' AND
      [articleName] NOT LIKE 'B_REPOSE DESIGNFOREVIG%' AND
      [articleName] NOT LIKE 'Retain 24 gavekort%' AND
      [articleName] NOT LIKE 'Diverse Vinding%' AND
      [articleName] NOT LIKE 'Frakt' AND
      [articleName] NOT LIKE 'SERVISE MATEUS' AND
      [articleName] NOT LIKE 'IHR LUNSJSERVIETTER 33X33CM VINDING' AND
      [articleName] NOT LIKE 'Diverse Glass%' AND
      [articleName] NOT LIKE 'MARIMEKKO LUNSJSERVIETTER 33X33CM VINDING' AND
      [articleName] NOT LIKE 'M_BLER VIPP' AND
      [articleName] NOT LIKE 'Diverse SERVISE%'

    ORDER BY
      articleStock.lastSold
    EOT;
  }

  private function get_query_include_common () {
    return <<<EOT
    SET LANGUAGE NORWEGIAN
    SELECT
      Brands.brandLabel AS Merke,
      Article.articleName AS Navn,
      DAY(articleStock.lastSold) AS Dato,
      CAST (stockQty AS INT) AS Antall,
      articleStock.StorageShelf AS Plasserng,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS Sist_Importert,
      Article.suppliers_art_no AS Lev_id

    FROM
      Article
      INNER JOIN articleStock ON Article.articleId = articleStock.articleId
      INNER JOIN Brands ON Article.brandId = Brands.brandId

    WHERE
      DATEPART(MONTH, articleStock.lastSold) = DATEPART(MONTH, CURRENT_TIMESTAMP) AND
      DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP) AND
      ArticleStatus = '0' AND Article.articleName NOT LIKE '[.]%' AND stockQty<='0'

    ORDER BY
      articleStock.lastSold
    EOT;
  }



  private function get_query_exlude_common_sort_brand () {
    return <<<EOT
    SET LANGUAGE NORWEGIAN
    SELECT
      Brands.brandLabel AS Merke,
      Article.articleName AS Navn,
      DAY(articleStock.lastSold) AS Dato,
      CAST (stockQty AS INT) AS Antall,
      articleStock.StorageShelf AS Plasserng,
      CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS Sist_Importert,
      Article.suppliers_art_no AS Lev_id

    FROM
      Article
      INNER JOIN articleStock ON Article.articleId = articleStock.articleId
      INNER JOIN Brands ON Article.brandId = Brands.brandId

    WHERE
      DATEPART(MONTH, articleStock.lastSold) = DATEPART(MONTH, CURRENT_TIMESTAMP) AND
      DATEPART(YEAR, articleStock.lastSold) = DATEPART(YEAR, CURRENT_TIMESTAMP) AND
      ArticleStatus = '0' AND Article.articleName NOT LIKE '[.]%' AND stockQty<='0' AND
      [articleName] NOT LIKE 'B_REPOSE DESIGNFOREVIG%' AND
      [articleName] NOT LIKE 'Retain 24 gavekort%' AND
      [articleName] NOT LIKE 'Diverse Vinding%' AND
      [articleName] NOT LIKE 'Frakt' AND
      [articleName] NOT LIKE 'SERVISE MATEUS' AND
      [articleName] NOT LIKE 'IHR LUNSJSERVIETTER 33X33CM VINDING' AND
      [articleName] NOT LIKE 'Diverse Glass%' AND
      [articleName] NOT LIKE 'MARIMEKKO LUNSJSERVIETTER 33X33CM VINDING' AND
      [articleName] NOT LIKE 'M_BLER VIPP' AND
      [articleName] NOT LIKE 'Diverse SERVISE%'

    ORDER BY
      Brands.brandLabel
    EOT;
  }

}
