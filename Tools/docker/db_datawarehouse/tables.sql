DROP TABLE IF EXISTS `articles`;
CREATE TABLE `articles` (
  `article_id` int(10) unsigned NOT NULL,
  `brand_id` int(10) unsigned DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  KEY `article_id` (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `barcodes`;
CREATE TABLE `barcodes` (
  `article_id` int(10) unsigned DEFAULT NULL,
  `barcode` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `brands`;
CREATE TABLE `brands` (
  `brand_id` int(10) unsigned NOT NULL,
  `brand_name` varchar(255) NOT NULL,
  KEY `brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `cip_cache`;
CREATE TABLE `cip_cache` (
  `mem_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `mem_key` varchar(255) NOT NULL,
  `mem_val` varchar(4096) NOT NULL
) ENGINE=MEMORY DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `imports`;
CREATE TABLE `imports` (
  `article_id` int(10) unsigned DEFAULT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  `import_qty` int(11) NOT NULL,
  `stock_qty` int(11) DEFAULT NULL,
  `stock_location` char(10) DEFAULT NULL,
  `supply_id` varchar(255) DEFAULT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `placement`;
CREATE TABLE `placement` (
  `article_id` int(10) unsigned NOT NULL,
  `stock_location` char(10) NOT NULL,
  `timestamp` char(30) NOT NULL,
  `yyyymmdd` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `placement_invalid`;
CREATE TABLE `placement_invalid` (
  `barcode` varchar(255) NOT NULL,
  `stock_location` char(10) NOT NULL,
  `timestamp` char(30) NOT NULL,
  `yyyymmdd` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `sales`;
CREATE TABLE `sales` (
  `article_id` int(10) unsigned NOT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  `sold_qty` int(11) NOT NULL,
  `date` char(10) NOT NULL,
  `time` char(5) NOT NULL,
  `price` decimal(18,2) DEFAULT NULL,
  `discount` decimal(18,2) DEFAULT NULL,
  `pay_method` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `sales_count`;
CREATE TABLE `sales_count` (
  `00` int(11) NOT NULL,
  `01` int(11) NOT NULL,
  `02` int(11) NOT NULL,
  `03` int(11) NOT NULL,
  `04` int(11) NOT NULL,
  `05` int(11) NOT NULL,
  `06` int(11) NOT NULL,
  `07` int(11) NOT NULL,
  `08` int(11) NOT NULL,
  `09` int(11) NOT NULL,
  `10` int(11) NOT NULL,
  `11` int(11) NOT NULL,
  `12` int(11) NOT NULL,
  `13` int(11) NOT NULL,
  `14` int(11) NOT NULL,
  `15` int(11) NOT NULL,
  `16` int(11) NOT NULL,
  `17` int(11) NOT NULL,
  `18` int(11) NOT NULL,
  `19` int(11) NOT NULL,
  `20` int(11) NOT NULL,
  `21` int(11) NOT NULL,
  `22` int(11) NOT NULL,
  `23` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `sales_hourly`;
CREATE TABLE `sales_hourly` (
  `00` int(11) NOT NULL,
  `01` int(11) NOT NULL,
  `02` int(11) NOT NULL,
  `03` int(11) NOT NULL,
  `04` int(11) NOT NULL,
  `05` int(11) NOT NULL,
  `06` int(11) NOT NULL,
  `07` int(11) NOT NULL,
  `08` int(11) NOT NULL,
  `09` int(11) NOT NULL,
  `10` int(11) NOT NULL,
  `11` int(11) NOT NULL,
  `12` int(11) NOT NULL,
  `13` int(11) NOT NULL,
  `14` int(11) NOT NULL,
  `15` int(11) NOT NULL,
  `16` int(11) NOT NULL,
  `17` int(11) NOT NULL,
  `18` int(11) NOT NULL,
  `19` int(11) NOT NULL,
  `20` int(11) NOT NULL,
  `21` int(11) NOT NULL,
  `22` int(11) NOT NULL,
  `23` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `soldout`;
CREATE TABLE `soldout` (
  `article_id` int(10) unsigned DEFAULT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  `stock_qty` int(11) DEFAULT NULL,
  `stock_location` varchar(255) DEFAULT NULL,
  `last_import` char(10) DEFAULT NULL,
  `supply_id` varchar(255) DEFAULT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `turnover_daily`;
CREATE TABLE `turnover_daily` (
  `sum` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `turnover_hourly`;
CREATE TABLE `turnover_hourly` (
  `00` int(11) NOT NULL,
  `01` int(11) NOT NULL,
  `02` int(11) NOT NULL,
  `03` int(11) NOT NULL,
  `04` int(11) NOT NULL,
  `05` int(11) NOT NULL,
  `06` int(11) NOT NULL,
  `07` int(11) NOT NULL,
  `08` int(11) NOT NULL,
  `09` int(11) NOT NULL,
  `10` int(11) NOT NULL,
  `11` int(11) NOT NULL,
  `12` int(11) NOT NULL,
  `13` int(11) NOT NULL,
  `14` int(11) NOT NULL,
  `15` int(11) NOT NULL,
  `16` int(11) NOT NULL,
  `17` int(11) NOT NULL,
  `18` int(11) NOT NULL,
  `19` int(11) NOT NULL,
  `20` int(11) NOT NULL,
  `21` int(11) NOT NULL,
  `22` int(11) NOT NULL,
  `23` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `chat`;
CREATE TABLE `chat` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `chat_by` varchar(32) NOT NULL,
  `chat_to` varchar(32),
  `chat_text` text NOT NULL,
  `chat_time` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (chat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
