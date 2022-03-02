<?php

require_once '../applications/Query.php';

class QueryFindBySearch extends QueryRetail {

  function __construct () {
    parent::__construct();
    $this->query = <<<EOT
    SELECT
      Article.articleId AS articleid,
      Brands.brandLabel AS brand,
      Article.articleName AS article,
      CAST (stockQty AS INT) AS quantity,
      articleStock.StorageShelf AS location,
      Article.suppliers_art_no AS supplyid
    FROM
      Article
    INNER JOIN
      articleStock ON Article.articleId = articleStock.articleId
    INNER JOIN
      Brands ON Article.brandId = Brands.brandId\n
    EOT;
  }

}

class QueryFindByBarcode extends QueryRetail {

  function __construct () {
    parent::__construct();
    // with the default start of query, we also at this part
    // so that we are able to use barcode in the where clause
    $this->query .= <<<EOT
    SELECT
      view_HIP_Productinfo.articleId,
      view_HIP_Productinfo.brandId,
      view_HIP_Productinfo.brandLabel,
      view_HIP_Productinfo.ArticleGroupName,
      view_HIP_Productinfo.articleName,
      view_HIP_Productinfo.articleUnitPrice,
      CAST (articleStock.stockQty AS INT) AS Antall,
      articleStock.StorageShelf AS Lagerplass,
      articleStock.lastSold AS Sist_Solgt,
      articleStock.lastReceivedFromSupplier AS Sist_Importert
    FROM
      view_HIP_Productinfo
    INNER JOIN
      ArticleEAN ON view_HIP_Productinfo.articleId = ArticleEAN.articleId
    INNER JOIN
      articleStock ON view_HIP_Productinfo.articleId = articleStock.articleId
    WHERE
      ArticleEAN.eanCode=(:barcode)
    EOT;
  }


  public function add_barcode ($part) {
    if(!(is_numeric($part))) {
      // barcode should be all numbers
      // also, no sql injection here, this is a simple way to avoid it
      echo "$part is not a barcode";
      exit(1);
    }
    $this->query .= <<<EOT
      ArticleEAN.eanCode = '$part'
    EOT;
  }

}
